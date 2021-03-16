__author__ = "aki"

from rest_framework import serializers
from master.models import User as UserTbl, get_user_by_id
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl
from v1.meter_data_management.serializers.schedule_log import ScheduleLogShortViewSerializer


class ScheduleLogReadCycleRevisitTaskViewSerializer(serializers.ModelSerializer):
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    schedule_log_id = ScheduleLogShortViewSerializer(many=False, source='get_schedule_log')
    meter_reader_detail = serializers.SerializerMethodField()
    task_detail = serializers.SerializerMethodField()

    def get_task_detail(self, route_task_assignment_tbl):
        task_list = []
        task_obj = [x for x in route_task_assignment_tbl.consumer_meter_json if x['is_active'] == True and
                    x['is_revisit'] == True]

        for task in task_obj:
            task_dict = {}
            if task['meter_reader_id'] == None:
                task_dict['meter_reader_id'] = task['meter_reader_id']
                task_dict['meter_reader_first_name'] = '-'
                task_dict['meter_reader_last_name'] = '-'
            else:
                meter_reader_obj = get_user_by_id(task['meter_reader_id'])
                task_dict['meter_reader_id'] = task['meter_reader_id']
                task_dict['meter_reader_first_name'] = meter_reader_obj.first_name
                task_dict['meter_reader_last_name'] = meter_reader_obj.last_name

            task_dict['meter_no'] = task['meter_no']
            task_dict['consumer_no'] = task['consumer_no']
            task_dict['status'] = task['status']
            task_list.append(task_dict)

        task_detail = {
            'task_obj': task_list
        }
        return task_detail

    def get_meter_reader_detail(self, route_task_assignment_tbl):
        meter_reader_obj = UserTbl.objects.filter(is_active=True)
        meter_reader_detail =[]
        for meter_reader in meter_reader_obj:
            meter_reader_dict = {
                'id_string': meter_reader.id_string,
                'first_name': meter_reader.first_name,
                'last_name': meter_reader.last_name,
                'phone_mobile': meter_reader.phone_mobile,
                'email': meter_reader.email,
                'route_task_assignment_count': RouteTaskAssignmentTbl.objects.filter(meter_reader_id=meter_reader.id,
                                                                                     schedule_log_id=route_task_assignment_tbl.schedule_log_id,
                                                                                     is_completed=False,
                                                                                     is_active=True).count(),
            }
            meter_reader_detail.append(meter_reader_dict)
        return meter_reader_detail

    class Meta:
        model = RouteTaskAssignmentTbl
        fields = ('id_string', 'read_cycle_id', 'route_id', 'schedule_log_id', 'task_detail', 'meter_reader_detail')

