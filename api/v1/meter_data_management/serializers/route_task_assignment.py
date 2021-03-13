__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.task.update_route_task_status import update_route_task_status
from v1.meter_data_management.task.assign_route_task import assign_route_task
from v1.meter_data_management.task.assign_partial_route_task import assign_partial_route_task
from v1.meter_data_management.task.de_assign_route_task import de_assign_route_task
from v1.userapp.serializers.user import UserShortViewSerializer
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl
from v1.meter_data_management.serializers.schedule_log import ScheduleLogShortViewSerializer
from v1.meter_data_management.views.common_function import set_route_task_assignment_validated_data


class RouteTaskAssignmentShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteTaskAssignmentTbl
        fields = ('id_string',)


class RouteTaskAssignmentViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    meter_reader_id = UserShortViewSerializer(many=False, source='get_meter_reader_name')
    schedule_log_id = ScheduleLogShortViewSerializer(many=False, source='get_schedule_log')
    dispatch_status = ChoiceField(choices=RouteTaskAssignmentTbl.DISPATCH_STATUS)
    task_detail = serializers.SerializerMethodField()

    def get_task_detail(self, route_task_assignment_tbl):
        meter_list = []
        task_obj = [x for x in route_task_assignment_tbl.consumer_meter_json if x['is_active'] == True and
                    x['status'] == 'ALLOCATED']

        for task in task_obj:
            meter_list.append(task['meter_no'])

        task_detail = {
            'task_count': len(task_obj),
            'task_obj': task_obj
        }
        update_route_task_status.delay(route_task_assignment_tbl.id, meter_list)
        return task_detail

    class Meta:
        model = RouteTaskAssignmentTbl
        fields = ('id_string', 'dispatch_status', 'assign_date', 'read_cycle_id', 'route_id', 'meter_reader_id',
                  'schedule_log_id', 'tenant', 'utility', 'task_detail')


class RouteTaskAssignmentSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=True)
    read_cycle_id = serializers.UUIDField(required=True)
    route_id = serializers.UUIDField(required=True)
    meter_reader_id = serializers.UUIDField(required=True)
    schedule_log_id = serializers.UUIDField(required=True)

    class Meta:
        model = RouteTaskAssignmentTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_route_task_assignment_validated_data(validated_data)
        try:
            route_task_assignment_obj = RouteTaskAssignmentTbl.objects.get(tenant=user.tenant,
                                                                              utility_id=validated_data['utility_id'],
                                                                              read_cycle_id=validated_data["read_cycle_id"],
                                                                              route_id=validated_data["route_id"],
                                                                              schedule_log_id=validated_data["schedule_log_id"],
                                                                              is_active=True)

            if route_task_assignment_obj.dispatch_status == 0 or route_task_assignment_obj.dispatch_status == 4:
                route_task_assignment_obj.meter_reader_id = validated_data["meter_reader_id"]
                route_task_assignment_obj.dispatch_status = 1
                route_task_assignment_obj.updated_date = timezone.now()
                route_task_assignment_obj.save()
                assign_partial_route_task.delay(route_task_assignment_obj.id)
                return route_task_assignment_obj
            if route_task_assignment_obj.dispatch_status == 2 or route_task_assignment_obj.dispatch_status == 3:
                route_task_assignment_obj.dispatch_status = 1
                route_task_assignment_obj.updated_date = timezone.now()
                route_task_assignment_obj.save()
                de_assign_route_task.delay(route_task_assignment_obj.id)
                return route_task_assignment_obj
            if route_task_assignment_obj.dispatch_status == 5:
                route_task_assignment_obj.dispatch_status = 1
                route_task_assignment_obj.updated_date = timezone.now()
                route_task_assignment_obj.save()
                assign_route_task.delay(route_task_assignment_obj.id)
                return route_task_assignment_obj
            if route_task_assignment_obj.dispatch_status == 6:
                route_task_assignment_obj.dispatch_status = 1
                route_task_assignment_obj.updated_date = timezone.now()
                route_task_assignment_obj.save()
                de_assign_route_task.delay(route_task_assignment_obj.id)
                return route_task_assignment_obj
        except RouteTaskAssignmentTbl.DoesNotExist:
            with transaction.atomic():
                route_task_assignment_obj = super(RouteTaskAssignmentSerializer, self).create(validated_data)
                route_task_assignment_obj.tenant = user.tenant
                route_task_assignment_obj.created_by = user.id
                route_task_assignment_obj.assign_date = timezone.now()
                route_task_assignment_obj.dispatch_status = 1
                route_task_assignment_obj.save()
                assign_route_task.delay(route_task_assignment_obj.id)
                return route_task_assignment_obj

    def update(self, instance, validated_data, user):
        validated_data = set_route_task_assignment_validated_data(validated_data)
        with transaction.atomic():
            route_task_assignment_obj = super(RouteTaskAssignmentSerializer, self).update(instance, validated_data)
            route_task_assignment_obj.tenant = user.tenant
            route_task_assignment_obj.updated_by = user.id
            route_task_assignment_obj.assign_date = timezone.now()
            route_task_assignment_obj.updated_date = timezone.now()
            route_task_assignment_obj.save()
            return route_task_assignment_obj
