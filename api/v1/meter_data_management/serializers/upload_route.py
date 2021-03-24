__author__ = "aki"

from django.db.models import Q
from django.db import transaction
from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.schedule import get_schedule_by_id
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id
from v1.meter_data_management.models.upload_route import UploadRoute as UploadRouteTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl
from v1.meter_data_management.serializers.schedule_log import ScheduleLogShortViewSerializer
from v1.meter_data_management.views.common_function import set_upload_route_validated_data


class UploadRouteViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    schedule_log_id = ScheduleLogShortViewSerializer(many=False, source='get_schedule_log')
    route_detail = serializers.SerializerMethodField()

    def get_route_detail(self, route_task_assignment_tbl):
        schedule_log_obj = get_schedule_log_by_id(route_task_assignment_tbl.schedule_log_id)
        schedule_obj = get_schedule_by_id(schedule_log_obj.schedule_id)

        total_consumer = ConsumerDetailTbl.objects.filter(schedule_log_id=route_task_assignment_tbl.schedule_log_id,
                                                          route_id=route_task_assignment_tbl.route_id, is_active=True).count()

        normal_reading = MeterReadingTbl.objects.filter(~Q(reading_status=3), is_active=True,
                                                        schedule_log_id=route_task_assignment_tbl.schedule_log_id,
                                                        route_id=route_task_assignment_tbl.route_id).count()

        completed_reading = MeterReadingTbl.objects.filter(reading_status=2, is_active=True,
                                                           schedule_log_id=route_task_assignment_tbl.schedule_log_id,
                                                           route_id=route_task_assignment_tbl.route_id).count()
        try:
            upload_route_obj = UploadRouteTbl.objects.get(schedule_log_id=route_task_assignment_tbl.schedule_log_id,
                                                          read_cycle_id=route_task_assignment_tbl.read_cycle_id,
                                                          route_id=route_task_assignment_tbl.route_id, is_active=True)
            status = upload_route_obj.get_state_display()
        except UploadRouteTbl.DoesNotExist:
            status = 'NOT-SENT'

        route_detail = {
            'upload_route_status': status,
            'schedule_name': schedule_obj.name,
            'total_consumer': total_consumer,
            'normal_reading': normal_reading,
            'completed_reading': completed_reading,
            'pending_reading': total_consumer - completed_reading
        }
        return route_detail

    class Meta:
        model = RouteTaskAssignmentTbl
        fields = ('id_string', 'read_cycle_id', 'route_id', 'schedule_log_id', 'tenant', 'utility', 'route_detail')


class UploadRouteSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=True)
    schedule_log_id = serializers.UUIDField(required=True)
    read_cycle_id = serializers.UUIDField(required=True)
    route_id = serializers.UUIDField(required=True)

    class Meta:
        model = UploadRouteTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        try:
            meter_reading_list = []
            validated_data = set_upload_route_validated_data(validated_data)
            try:
                upload_route_obj = UploadRouteTbl.objects.get(tenant=user.tenant, utility_id=validated_data['utility_id'],
                                                              schedule_log_id=validated_data["schedule_log_id"],
                                                              read_cycle_id=validated_data["read_cycle_id"],
                                                              route_id=validated_data["route_id"], is_active=True)
            except UploadRouteTbl.DoesNotExist:
                with transaction.atomic():
                    upload_route_obj = super(UploadRouteSerializer, self).create(validated_data)
                    upload_route_obj.tenant = user.tenant
                    upload_route_obj.created_by = user.id
                    upload_route_obj.save()

            upload_route_obj = upload_route_obj

            meter_reading_obj = MeterReadingTbl.objects.filter(schedule_log_id=upload_route_obj.schedule_log_id,
                                                               read_cycle_id=upload_route_obj.read_cycle_id,
                                                               route_id=upload_route_obj.route_id, is_active=True)
            for meter_reading in meter_reading_obj:
                meter_reading_list.append(
                    {
                        'consumer_no': meter_reading.consumer_no,
                        'meter_no': meter_reading.meter_no,
                        'current_reading': meter_reading.current_meter_reading_v2,
                    }
                )
            # todo API call
            upload_route_obj.state = 2
            upload_route_obj.save()
            print(meter_reading_list)
            return True
        except Exception as ex:
            upload_route_obj.state = 5
            upload_route_obj.save()
            return False
