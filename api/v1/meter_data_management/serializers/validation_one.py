__author__ = "aki"

from rest_framework import serializers
from django.db.models import Q
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.models.meter_status import get_meter_status_by_id
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id, get_read_cycle_by_id_string
from v1.meter_data_management.models.reader_status import get_reader_status_by_id
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id_string
from v1.meter_data_management.models.validation_assignments import ValidationAssignment as ValidationAssignmentTbl


class ValidationOneViewSerializer(serializers.ModelSerializer):
    reading_status = ChoiceField(choices=MeterReadingTbl.READING_STATUS)
    additional_details = serializers.SerializerMethodField()

    def get_meter_image_url(self, meter_reading_tbl):
        request = self.context.get('request')
        if meter_reading_tbl.meter_image:
            meter_image_url = request.build_absolute_uri(meter_reading_tbl.meter_image.url)
        else:
            meter_image_url = ''
        return meter_image_url

    def get_additional_details(self, meter_reading_tbl):
        read_cycle_list = []

        user_obj = get_user_by_id_string(self.context.get('user_id_string'))
        schedule_log_obj = get_schedule_log_by_id_string(self.context.get('schedule_log_id_string'))
        read_cycle_obj = get_read_cycle_by_id_string(self.context.get('read_cycle_id_string'))

        meter_status_obj = get_meter_status_by_id(meter_reading_tbl.meter_status_id)
        reader_status_obj = get_reader_status_by_id(meter_reading_tbl.reader_status_id)

        validation_assignment_obj = ValidationAssignmentTbl.objects.filter(validator1_id=user_obj.id, is_active=True)

        total_reading = MeterReadingTbl.objects.filter(~Q(reading_status=3), validator_one_id=user_obj.id,
                                                       read_cycle_id=read_cycle_obj.id,
                                                       schedule_log_id=schedule_log_obj.id,
                                                       is_active=True, is_duplicate=False).count()

        completed_reading = MeterReadingTbl.objects.filter(~Q(reading_status=3), validator_one_id=user_obj.id,
                                                           read_cycle_id=read_cycle_obj.id, is_validated=True,
                                                           schedule_log_id=schedule_log_obj.id,
                                                           is_active=True, is_duplicate=False).count()

        for validation_assignment in validation_assignment_obj:
            read_cycle_obj = get_read_cycle_by_id(validation_assignment.read_cycle_id)
            read_cycle_list.append({
                'name': read_cycle_obj.name,
                'id_string': read_cycle_obj.id_string,
            })

        additional_details= {
            'meter_status_id_string':meter_status_obj.id_string,
            'reader_status_id_string':reader_status_obj.id_string,
            'total_reading': total_reading,
            'completed_reading': completed_reading,
            'pending_reading': total_reading - completed_reading,
            'read_cycle_list': read_cycle_list,
        }

        return additional_details

    class Meta:
        model = MeterReadingTbl
        fields = ('id_string', 'reading_status', 'consumer_no', 'meter_no', 'current_meter_reading', 'meter_image',
                  'additional_details', 'meter_reading_json', 'additional_parameter_json')