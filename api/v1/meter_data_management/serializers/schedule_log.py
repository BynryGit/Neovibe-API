__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.views.settings_reader import SettingReader
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.schedule_log import ScheduleLog as ScheduleLogTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.schedule import ScheduleShortViewSerializer
from v1.utility.serializers.utility_product import UtilityProductShortViewSerializer
setting_reader = SettingReader()


class ScheduleLogViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    schedule_id = ScheduleShortViewSerializer(many=False, source='get_schedule_name')
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    activity_type_id = GlobalLookupShortViewSerializer(many=False, source='get_activity_type')
    recurring_id = GlobalLookupShortViewSerializer(many=False, source='get_recurring_name')
    utility_product_id = UtilityProductShortViewSerializer(many=False, source='get_utility_product_type_name')
    date_and_time = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    schedule_log_status = ChoiceField(choices=ScheduleLogTbl.SCHEDULE_LOG_STATUS)

    class Meta:
        model = ScheduleLogTbl
        fields = ('id_string', 'schedule_log_status', 'date_and_time', 'created_date', 'updated_date', 'created_by',
                  'updated_by', 'schedule_id', 'read_cycle_id', 'activity_type_id', 'recurring_id', 'utility_product_id',
                  'tenant', 'utility')
