__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.consumer_detail import ConsumerDetail
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment
from v1.meter_data_management.models.schedule_log import ScheduleLog as ScheduleLogTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.schedule import ScheduleShortViewSerializer
from v1.utility.serializers.utility_product import UtilityProductShortViewSerializer


class ScheduleLogViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    schedule_id = ScheduleShortViewSerializer(many=False, source='get_schedule_name')
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    activity_type_id = GlobalLookupShortViewSerializer(many=False, source='get_activity_type')
    recurring_id = GlobalLookupShortViewSerializer(many=False, source='get_recurring_name')
    utility_product_id = UtilityProductShortViewSerializer(many=False, source='get_utility_product_name')
    schedule_log_status = ChoiceField(choices=ScheduleLogTbl.SCHEDULE_LOG_STATUS)
    route_detail = serializers.SerializerMethodField()
    total_consumer = serializers.SerializerMethodField()

    def get_route_detail(self, schedule_log_tbl):
        total_route = get_read_cycle_by_id(id=schedule_log_tbl.read_cycle_id)
        route_detail = {
            'total_route' : len(total_route.route_json),
            'started_route': RouteTaskAssignment.objects.filter(dispatch_status=2, is_active=True).count(),
            'dispatch_route': RouteTaskAssignment.objects.filter(dispatch_status=3, is_active=True).count(),
            'completed_route': RouteTaskAssignment.objects.filter(dispatch_status=3, is_completed=True, is_active=True).count(),
        }
        return route_detail

    def get_total_consumer(self, schedule_log_tbl):
        return ConsumerDetail.objects.filter(schedule_log_id=schedule_log_tbl.id, is_active=True).count()

    class Meta:
        model = ScheduleLogTbl
        fields = ('id_string', 'schedule_log_status', 'date_and_time', 'created_date', 'updated_date', 'created_by',
                  'updated_by', 'total_consumer', 'route_detail', 'schedule_id', 'read_cycle_id', 'activity_type_id',
                  'recurring_id', 'utility_product_id', 'tenant', 'utility')
