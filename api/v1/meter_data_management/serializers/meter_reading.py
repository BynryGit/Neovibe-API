__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.route_task_assignment import get_route_task_assignment_by_id
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.schedule_log import ScheduleLogShortViewSerializer
from v1.meter_data_management.views.common_function import set_meter_reading_validated_data


class MeterReadingShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeterReadingTbl
        fields = ('id_string', 'consumer_no', 'meter_no')


class MeterReadingViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    schedule_log_id = ScheduleLogShortViewSerializer(many=False, source='get_schedule_log_name')
    reading_status = ChoiceField(choices=MeterReadingTbl.READING_STATUS)

    def get_meter_image_url(self, meter_reading_tbl):
        request = self.context.get('request')
        if meter_reading_tbl.meter_image:
            meter_image_url = request.build_absolute_uri(meter_reading_tbl.meter_image.url)
        else:
            meter_image_url = ''
        return meter_image_url

    class Meta:
        model = MeterReadingTbl
        fields = ('__all__')


class MeterReadingSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=True)
    consumer_detail_id = serializers.UUIDField(required=True)
    route_task_assignment_id = serializers.UUIDField(required=True)
    read_cycle_id = serializers.UUIDField(required=False)
    route_id = serializers.UUIDField(required=False)
    meter_reader_id = serializers.UUIDField(required=False)
    meter_status_id = serializers.UUIDField(required=False)
    reader_status_id = serializers.UUIDField(required=False)
    utility_product_id = serializers.UUIDField(required=False)

    class Meta:
        model = MeterReadingTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_meter_reading_validated_data(validated_data)
        try:
            meter_reading_obj = MeterReadingTbl.objects.get(tenant=user.tenant,
                                                            utility_id=validated_data["utility_id"],
                                                            route_task_assignment_id=validated_data["route_task_assignment_id"],
                                                            consumer_detail_id=validated_data['consumer_detail_id'],
                                                            is_active=True)
            return meter_reading_obj
        except Exception:
            try:
                with transaction.atomic():
                    meter_reading_obj = super(MeterReadingSerializer, self).create(validated_data)
                    meter_reading_obj.tenant = user.tenant
                    route_task_assignment_obj = get_route_task_assignment_by_id(meter_reading_obj.route_task_assignment_id)
                    meter_reading_obj.read_cycle_id = route_task_assignment_obj.read_cycle_id
                    meter_reading_obj.route_id = route_task_assignment_obj.route_id
                    meter_reading_obj.schedule_log_id = route_task_assignment_obj.schedule_log_id
                    meter_reading_obj.meter_reader_id = route_task_assignment_obj.meter_reader_id
                    meter_reading_obj.created_by = user.id

                    meter_reading_obj.save()

                    task_obj = [x for x in route_task_assignment_obj.consumer_meter_json if x['is_active'] == True and
                                x['meter_no'] == validated_data['meter_no']]

                    for task in task_obj:
                        task['status'] = 'COMPLETED'
                        task['is_completed'] = True
                        task['is_revisit'] = False

                    route_task_assignment_obj.save()

                    return meter_reading_obj
            except Exception as ex:
                print(ex)
                return None

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            meter_reading_obj = super(MeterReadingSerializer, self).update(instance, validated_data)
            meter_reading_obj.tenant = user.tenant
            meter_reading_obj.updated_by = user.id
            meter_reading_obj.updated_date = timezone.now()
            meter_reading_obj.save()
            return meter_reading_obj