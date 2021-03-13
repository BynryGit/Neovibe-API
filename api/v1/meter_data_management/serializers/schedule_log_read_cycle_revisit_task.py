__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.userapp.serializers.user import UserShortViewSerializer
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl
from v1.meter_data_management.serializers.schedule_log import ScheduleLogShortViewSerializer


class ScheduleLogReadCycleRevisitTaskViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    meter_reader_id = UserShortViewSerializer(many=False, source='get_meter_reader_name')
    schedule_log_id = ScheduleLogShortViewSerializer(many=False, source='get_schedule_log')
    dispatch_status = ChoiceField(choices=RouteTaskAssignmentTbl.DISPATCH_STATUS)
    task_detail = serializers.SerializerMethodField()

    def get_task_detail(self, route_task_assignment_tbl):
        task_list = []
        task_obj = [x for x in route_task_assignment_tbl.consumer_meter_json if x['is_active'] == True and
                    x['status'] == 'REVISIT']

        for task in task_obj:
            task_dict = {}
            task_dict['meter_no'] = task['meter_no']
            task_dict['consumer_no'] = task['consumer_no']
            task_dict['status'] = task['status']
            task_list.append(task_dict)

        task_detail = {
            'task_obj': task_list
        }
        return task_detail

    class Meta:
        model = RouteTaskAssignmentTbl
        fields = ('id_string', 'dispatch_status', 'assign_date', 'read_cycle_id', 'route_id', 'meter_reader_id',
                  'schedule_log_id', 'tenant', 'utility', 'task_detail')

