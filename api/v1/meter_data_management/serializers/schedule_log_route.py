__author__ = "aki"

from rest_framework import serializers
from master.models import User as UserTbl, get_user_by_id
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.consumer_detail import ConsumerDetail
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route import Route as RouteTbl
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment, ROUTE_TASK_ASSIGNMENT_STATUS_DICT
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id_string
from v1.userapp.models.role import Role as RoleTbl
from v1.userapp.models.user_role import get_user_role_by_role_id


class ScheduleLogRouteViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    route_detail = serializers.SerializerMethodField()
    meter_reader_detail = serializers.SerializerMethodField()
    other_detail = serializers.SerializerMethodField()

    # Todo separate API for meter reader list using raw query
    def get_meter_reader_detail(self, route_tbl):
        schedule_log_id = get_schedule_log_by_id_string(self.context.get('schedule_log_id'))
        role_obj = RoleTbl.objects.get(utility=schedule_log_id.utility, role_ID='Meter_Reader')
        user_role_obj = get_user_role_by_role_id(role_obj.id)
        meter_reader_obj = UserTbl.objects.filter(id__in=[user_role.user_id for user_role in user_role_obj],
                                                  is_active=True)
        meter_reader_detail =[]
        for meter_reader in meter_reader_obj:
            meter_reader_detail.append(
                {
                    'id_string': meter_reader.id_string,
                    'first_name': meter_reader.first_name,
                    'last_name': meter_reader.last_name,
                    'phone_mobile': meter_reader.phone_mobile,
                    'email': meter_reader.email,
                    'route_task_assignment_count': RouteTaskAssignment.objects.filter(meter_reader_id=meter_reader.id,
                                                                                      is_completed=False,
                                                                                      is_active=True).count(),
                }
            )
        return meter_reader_detail

    def get_route_detail(self, route_tbl):
        schedule_log_id = get_schedule_log_by_id_string(self.context.get('schedule_log_id'))
        total_consumer = ConsumerDetail.objects.filter(utility=schedule_log_id.utility,
                                                       schedule_log_id=schedule_log_id.id, route_id=route_tbl.id,
                                                       state=0, is_active=True).count()
        try:
            route_task_assignment_obj = RouteTaskAssignment.objects.get(schedule_log_id=schedule_log_id.id,
                                                                        route_id=route_tbl.id, is_active=True)
            if route_task_assignment_obj.consumer_meter_json == None:
                complete_task_obj = 0
            else:
                complete_task_obj = [x for x in route_task_assignment_obj.consumer_meter_json if
                                     x['is_active'] == True and
                                     x['is_completed'] == True and x['is_revisit'] == False]
                complete_task_obj = len(complete_task_obj)

            if route_task_assignment_obj.meter_reader_id == None:
                meter_reader_first_name = 'NA'
                meter_reader_last_name = ''
                meter_reader_task_count = 0
                assign_date = route_task_assignment_obj.assign_date
                total_reading = complete_task_obj
                state = route_task_assignment_obj.get_state_display()
            else:
                meter_reader_obj = get_user_by_id(route_task_assignment_obj.meter_reader_id)
                meter_reader_first_name = meter_reader_obj.first_name
                meter_reader_last_name = meter_reader_obj.last_name
                assign_date = route_task_assignment_obj.assign_date
                total_reading = complete_task_obj
                state = route_task_assignment_obj.get_state_display()
                meter_reader_task_count = RouteTaskAssignment.objects.filter(meter_reader_id=meter_reader_obj.id,
                                                                             schedule_log_id=schedule_log_id.id,
                                                                             is_completed=False, is_active=True).count()
                try:
                    if total_consumer == total_reading:
                        route_task_assignment_obj.change_state(ROUTE_TASK_ASSIGNMENT_STATUS_DICT["COMPLETED"])
                        route_task_assignment_obj.is_completed=True
                        route_task_assignment_obj.save()
                except:
                    pass
        except:
            meter_reader_first_name = 'NA'
            meter_reader_last_name = ''
            assign_date = 'NA'
            state = 'NOT-DISPATCHED'
            meter_reader_task_count = 0
            total_reading = 0

        route_detail = {
            'total_consumer': total_consumer,
            'total_reading': total_reading,
            'meter_reader_first_name': meter_reader_first_name,
            'meter_reader_last_name': meter_reader_last_name,
            'assign_date': assign_date,
            'state': state,
            'meter_reader_task_count': meter_reader_task_count
        }
        return route_detail

    def get_other_detail(self, route_tbl):
        schedule_log_id = get_schedule_log_by_id_string(self.context.get('schedule_log_id'))
        read_cycle_id = get_read_cycle_by_id(schedule_log_id.read_cycle_id)

        other_detail = {
            'schedule_log_id_string': self.context.get('schedule_log_id'),
            'read_cycle_id_string': read_cycle_id.id_string,
        }
        return other_detail

    class Meta:
        model = RouteTbl
        fields = ('id_string', 'label', 'name', 'description', 'created_date', 'updated_date', 'created_by',
                  'updated_by', 'meter_reader_detail', 'route_detail', 'other_detail', 'premises_json', 'filter_json',
                  'tenant', 'utility')
