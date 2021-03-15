__author__ = "aki"

from rest_framework import serializers

from v1.commonapp.models.meter_status import get_meter_status_by_name
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.schedule_log import ScheduleLog as ScheduleLogTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.schedule import ScheduleShortViewSerializer
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl


class ValidationScheduleLogShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleLogTbl
        fields = ('id_string',)


class ValidationScheduleLogViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    schedule_id = ScheduleShortViewSerializer(many=False, source='get_schedule_name')
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    meter_reading_detail = serializers.SerializerMethodField()

    def get_meter_reading_detail(self, schedule_log_tbl):
        total_completed_task = 0
        meter_status_obj = get_meter_status_by_name('RCNT')
        consumer_obj = ConsumerDetailTbl.objects.filter(schedule_log_id=schedule_log_tbl.id, is_active=True).count()
        meter_reading_obj = MeterReadingTbl.objects.filter(schedule_log_id=schedule_log_tbl.id)
        route_task_assignment_obj = RouteTaskAssignmentTbl.objects.filter(schedule_log_id=schedule_log_tbl.id,
                                                                          is_active=True)

        for route_task in route_task_assignment_obj:
            complete_task_obj = [x for x in route_task.consumer_meter_json if
                                 x['is_active'] == True and x['is_completed'] == True]
            total_completed_task = total_completed_task + len(complete_task_obj)

        meter_reading_detail = {
            'total_consumer' : consumer_obj,
            'received_reading' : total_completed_task,
            'pending_reading' : consumer_obj - total_completed_task,
            'rcnt_reading' : meter_reading_obj.filter(reading_status=2, meter_status_id=meter_status_obj.id, is_active=True).count(),
            'duplicate_reading' : meter_reading_obj.filter(is_duplicate=True, is_active=False).count(),
            'validation_one' : meter_reading_obj.filter(reading_status=0, is_active=True).count(),
            'validation_two' : meter_reading_obj.filter(reading_status=1, is_assign_to_v1=True, is_active=True).count(),
            'completed_reading': meter_reading_obj.filter(reading_status=2, is_assign_to_v2=True, is_active=True).count(),
        }
        return meter_reading_detail

    class Meta:
        model = ScheduleLogTbl
        fields = ('id_string', 'meter_reading_detail', 'schedule_id', 'read_cycle_id', 'tenant', 'utility')
