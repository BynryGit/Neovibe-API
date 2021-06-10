__author__ = "aki"

from rest_framework import serializers
from master.models import get_user_by_id_string
from django.db.models import Q
from v1.commonapp.models.meter_status import get_meter_status_by_name
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.new_consumer_detail import NewConsumerDetail as NewConsumerDetailTbl
from v1.meter_data_management.models.schedule_log import ScheduleLog as ScheduleLogTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.schedule import ScheduleShortViewSerializer
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl
from v1.userapp.models.role import Role as RoleTbl
from v1.userapp.models.user_role import get_user_role_by_user_id


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
        v1_flag = False
        v2_flag = False
        role_list = []
        total_completed_task = 0
        meter_status_obj = get_meter_status_by_name('RCNT')

        user_obj = get_user_by_id_string(self.context.get('user_id_string'))
        user_role_obj = get_user_role_by_user_id(user_obj.id)
        role_obj = RoleTbl.objects.filter(id__in=[user_role.role_id for user_role in user_role_obj], is_active=True)

        for role in role_obj:
            role_list.append(role.role_ID)

        consumer_count = ConsumerDetailTbl.objects.filter(schedule_log_id=schedule_log_tbl.id,
                                                          utility_product_id=schedule_log_tbl.utility_product_id,
                                                          state=0, is_active=True).count()

        v1_count = MeterReadingTbl.objects.filter(schedule_log_id=schedule_log_tbl.id, reading_status=0,
                                                  is_assign_to_v1=True, is_active=True).count()

        v2_count = MeterReadingTbl.objects.filter(schedule_log_id=schedule_log_tbl.id, reading_status=1,
                                                  is_assign_to_v2=True, is_active=True).count()

        assignment_count = MeterReadingTbl.objects.filter(Q(validator_one_id=user_obj.id) |
                                                          Q(validator_two_id=user_obj.id),
                                                          schedule_log_id=schedule_log_tbl.id,
                                                          is_active=True).count()

        if assignment_count:
            if 'Validator_One' in role_list:
                v1_flag = True
            elif 'Validator_Two' in role_list:
                v2_flag = True
            else:
                v1_flag = False
                v2_flag = False
        else:
            v1_flag = False
            v2_flag = False

        route_task_assignment_obj = RouteTaskAssignmentTbl.objects.filter(schedule_log_id=schedule_log_tbl.id,
                                                                          is_active=True)

        for route_task in route_task_assignment_obj:
            complete_task_obj = [x for x in route_task.consumer_meter_json if
                                 x['is_active'] == True and x['is_completed'] == True]
            total_completed_task = total_completed_task + len(complete_task_obj)

        meter_reading_detail = {
            'total_consumer': consumer_count,
            'received_reading': total_completed_task,
            'pending_reading': consumer_count - total_completed_task,
            'rcnt_reading': MeterReadingTbl.objects.filter(schedule_log_id=schedule_log_tbl.id, reading_status=2,
                                                           meter_status_id=meter_status_obj.id, is_active=True).count(),
            'duplicate_reading': MeterReadingTbl.objects.filter(schedule_log_id=schedule_log_tbl.id, is_duplicate=True,
                                                                is_active=False).count(),
            'validation_one': v1_count,
            'validation_two': v2_count,
            'new_consumer': NewConsumerDetailTbl.objects.filter(schedule_log_id=schedule_log_tbl.id, is_discard=False,
                                                                is_confirmed=False, is_active=True).count(),
            'completed_reading': MeterReadingTbl.objects.filter(schedule_log_id=schedule_log_tbl.id, reading_status=2,
                                                                is_active=True).count(),
            'v1_flag': v1_flag,
            'v2_flag': v2_flag
        }
        return meter_reading_detail

    class Meta:
        model = ScheduleLogTbl
        fields = ('id_string', 'meter_reading_detail', 'schedule_id', 'read_cycle_id', 'tenant', 'utility')
