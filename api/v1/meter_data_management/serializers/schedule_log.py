__author__ = "aki"

from rest_framework import serializers
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.schedule_log import ScheduleLog as ScheduleLogTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.schedule import ScheduleShortViewSerializer


class ScheduleLogViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    schedule_id = ScheduleShortViewSerializer(many=False, source='get_schedule_name')
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    activity_type_id = GlobalLookupShortViewSerializer(many=False, source='get_activity_type')
    date_and_time = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    schedule_log_status = ChoiceField(choices=ScheduleLogTbl.SCHEDULE_LOG_STATUS)

    class Meta:
        model = ScheduleLogTbl
        fields = ('id_string', 'schedule_log_status', 'is_recurring', 'date_and_time', 'created_date', 'updated_date',
                  'created_by', 'updated_by', 'schedule_id', 'read_cycle_id', 'activity_type_id', 'tenant', 'utility')
