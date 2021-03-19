__author__ = "aki"

from rest_framework import serializers
from django.db.models import Q
from master.models import get_user_by_id_string, get_user_by_id
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.commonapp.models.meter_status import get_meter_status_by_id
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.meter_data_management.models.consumer_detail import get_consumer_detail_by_id
from v1.meter_data_management.models.meter import get_meter_by_id
from v1.meter_data_management.models.meter_make import get_meter_make_by_id
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id, get_read_cycle_by_id_string
from v1.meter_data_management.models.reader_status import get_reader_status_by_id
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id_string
from v1.meter_data_management.models.validation_assignments import ValidationAssignment as ValidationAssignmentTbl
from v1.meter_data_management.serializers.schedule_log import ScheduleLogShortViewSerializer


class ValidationOneViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    schedule_log_id = ScheduleLogShortViewSerializer(many=False, source='get_schedule_log_name')
    reading_status = ChoiceField(choices=MeterReadingTbl.READING_STATUS)
    additional_details = serializers.SerializerMethodField()
    meter_details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    def get_meter_image_url(self, meter_reading_tbl):
        request = self.context.get('request')
        if meter_reading_tbl.meter_image:
            meter_image_url = request.build_absolute_uri(meter_reading_tbl.meter_image.url)
        else:
            meter_image_url = ''
        return meter_image_url

    def get_meter_details(self, meter_reading_tbl):
        consumer_detail_obj = get_consumer_detail_by_id(meter_reading_tbl.consumer_detail_id)
        meter_obj = get_meter_by_id(consumer_detail_obj.meter_id)
        meter_make_obj = get_meter_make_by_id(id=meter_obj.meter_make_id)
        meter_details = {
            'meter_no': meter_obj.meter_no,
            'meter_make': meter_make_obj.name,
            'meter_digit': meter_obj.meter_digit,
            'install_date': meter_obj.install_date,
        }
        return meter_details

    def get_user_details(self, meter_reading_tbl):
        consumer_detail_obj = get_consumer_detail_by_id(meter_reading_tbl.consumer_detail_id)
        consumer_master_obj = get_consumer_by_id(consumer_detail_obj.consumer_id)
        mr_object = get_user_by_id(meter_reading_tbl.meter_reader_id)
        validator_one_object = get_user_by_id(meter_reading_tbl.meter_reader_id)
        user_details = {
            'consumer_no': consumer_master_obj.consumer_no,
            'consumer_name': 'Na',
            'consumer_email': consumer_master_obj.email_id,
            'consumer_phone_mobile': consumer_master_obj.phone_mobile,
            'consumer_status': consumer_master_obj.get_state_display(),
            'consumer_address': consumer_master_obj.billing_address_line_1,
            'mr_name': mr_object.first_name + ' ' + mr_object.last_name,
            'mr_email': mr_object.email,
            'mr_phone_mobile': mr_object.phone_mobile,
            'v1_name': validator_one_object.first_name + ' ' + validator_one_object.last_name,
            'v1_email': validator_one_object.email,
            'v1_phone_mobile': validator_one_object.phone_mobile,
        }
        return user_details

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
                'label': read_cycle_obj.label,
                'id_string': read_cycle_obj.id_string,
            })

        additional_details= {
            'meter_status_id_string':meter_status_obj.id_string,
            'meter_status_name':meter_status_obj.name,
            'reader_status_id_string':reader_status_obj.id_string,
            'reader_status_name':reader_status_obj.name,
            'total_reading': total_reading,
            'completed_reading': completed_reading,
            'pending_reading': total_reading - completed_reading,
            'read_cycle_list': read_cycle_list,
        }

        return additional_details

    class Meta:
        model = MeterReadingTbl
        fields = ('id_string', 'reading_status', 'consumer_no', 'meter_no', 'current_meter_reading', 'is_meter_matching',
                  'is_reading_matching', 'is_validated', 'meter_image', 'meter_details', 'user_details',
                  'additional_details', 'meter_reading_json', 'additional_parameter_json', 'read_cycle_id',
                  'route_id', 'schedule_log_id', 'tenant', 'utility')