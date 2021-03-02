__author__ = "aki"

from rest_framework import serializers

from master.models import User
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.consumer_detail import ConsumerDetail
from v1.meter_data_management.models.route import Route as RouteTbl
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id_string


class ScheduleLogRouteViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    route_detail = serializers.SerializerMethodField()
    meter_reader_detail = serializers.SerializerMethodField()

    def get_meter_reader_detail(self, route_tbl):
        schedule_log_id = get_schedule_log_by_id_string(self.context.get('schedule_log_id'))
        meter_reader_obj = User.objects.filter(is_active=True)
        meter_reader_detail =[]
        for meter_reader in meter_reader_obj:
            meter_reader_dict = {
                'id_string': meter_reader.id_string,
                'first_name': meter_reader.first_name,
                'last_name': meter_reader.last_name,
                'phone_mobile': meter_reader.phone_mobile,
                'email': meter_reader.email,
                'route_task_assignment_count': RouteTaskAssignment.objects.filter(meter_reader_id=meter_reader.id,
                                                                                  schedule_log_id=schedule_log_id.id,
                                                                                  is_completed=False, is_active=True).count(),
            }
            meter_reader_detail.append(meter_reader_dict)
        return meter_reader_detail

    def get_route_detail(self, route_tbl):
        schedule_log_id = get_schedule_log_by_id_string(self.context.get('schedule_log_id'))
        try:
            route_task_assignment_obj = RouteTaskAssignment.objects.get(schedule_log_id=schedule_log_id.id,
                                                                        route_id=route_tbl.id, is_active=True)
        except:
            route_task_assignment_obj = False

        if route_task_assignment_obj == False:
            meter_reader = 'NA'
            assign_date = 'NA'
            dispatch_status = 'NOT-DISPATCHED'
        else:
            meter_reader = route_task_assignment_obj.meter_reader_id
            assign_date = route_task_assignment_obj.assign_date
            dispatch_status = ChoiceField(choices=route_task_assignment_obj.DISPATCH_STATUS)

        route_detail = {
            'total_consumer': ConsumerDetail.objects.filter(schedule_log_id=schedule_log_id.id, route_id=route_tbl.id,
                                                             is_active=True).count(),
            'total_reading': RouteTaskAssignment.objects.filter(consumer_meter_json__contains=[{'status':'completed'}], is_active=True).count(),
            'meter_reader': meter_reader,
            'assign_date': assign_date,
            'dispatch_status': dispatch_status
        }
        return route_detail

    class Meta:
        model = RouteTbl
        fields = ('id_string', 'label', 'name', 'description', 'created_date', 'updated_date', 'created_by',
                  'updated_by', 'meter_reader_detail', 'route_detail', 'premises_json', 'filter_json', 'tenant',
                  'utility')
