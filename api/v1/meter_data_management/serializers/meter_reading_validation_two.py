__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.views.common_function import set_meter_reading_validation_two_validated_data


class MeterReadingValidationTwoSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=True)
    meter_status_v2_id = serializers.UUIDField(required=True)
    reader_status_v2_id = serializers.UUIDField(required=True)

    class Meta:
        model = MeterReadingTbl
        fields = ('__all__')

    def update(self, instance, validated_data, user):
        validated_data = set_meter_reading_validation_two_validated_data(validated_data)
        try:
            with transaction.atomic():
                meter_reading_obj = MeterReadingTbl.objects.get(id=instance.id)

                duplicate_meter_reading_obj = MeterReadingTbl.objects.filter(
                    schedule_log_id=meter_reading_obj.schedule_log_id,
                    consumer_detail_id=meter_reading_obj.consumer_detail_id,
                    route_task_assignment_id=meter_reading_obj.route_task_assignment_id,
                    is_active=True).exclude(id=meter_reading_obj.id)

                if duplicate_meter_reading_obj:
                    meter_reading_obj.is_active = False
                    meter_reading_obj.is_duplicate = True
                    meter_reading_obj.reading_status = 1
                    meter_reading_obj.save()
                    return False
                    # todo send return response of duplication
                else:
                    meter_reading_obj.is_validated = True
                    meter_reading_obj.reading_status = 2
                    meter_reading_obj.meter_status_v2_id = validated_data["meter_status_v2_id"]
                    meter_reading_obj.reader_status_v2_id = validated_data["reader_status_v2_id"]
                    meter_reading_obj.current_meter_reading_v2 = validated_data["current_meter_reading_v2"]
                    meter_reading_obj.updated_by = user.id
                    meter_reading_obj.updated_date = timezone.now()
                    meter_reading_obj.save()
                return meter_reading_obj
        except MeterReadingTbl.DoesNotExist:
            return False

