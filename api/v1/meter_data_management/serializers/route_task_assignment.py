__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, ROUTE_TASK_ASSIGNMENT_ALREADY_EXIST
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl


class RouteTaskAssignmentShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteTaskAssignmentTbl
        fields = ('id_string',)


class RouteTaskAssignmentViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    # meter_reader_id = (many=False, source='get_meter_reader_name')
    dispatch_status = ChoiceField(choices=RouteTaskAssignmentTbl.DISPATCH_STATUS)

    class Meta:
        model = RouteTaskAssignmentTbl
        fields = ('__all__')


class RouteTaskAssignmentSerializer(serializers.ModelSerializer):
    read_cycle_id = serializers.UUIDField(required=True)
    route_id = serializers.UUIDField(required=True)

    class Meta:
        model = RouteTaskAssignmentTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        # validated_data = set_meter_reading_validated_data(validated_data)
        if RouteTaskAssignmentTbl.objects.filter(tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException(ROUTE_TASK_ASSIGNMENT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            route_task_assignment_obj = super(RouteTaskAssignmentSerializer, self).create(validated_data)
            route_task_assignment_obj.tenant = user.tenant
            route_task_assignment_obj.created_by = user.id
            route_task_assignment_obj.save()
            return route_task_assignment_obj

    def update(self, instance, validated_data, user):
        # validated_data = set_meter_reading_validated_data(validated_data)
        with transaction.atomic():
            route_task_assignment_obj = super(RouteTaskAssignmentSerializer, self).update(instance, validated_data)
            route_task_assignment_obj.tenant = user.tenant
            route_task_assignment_obj.updated_by = user.id
            route_task_assignment_obj.updated_date = timezone.now()
            route_task_assignment_obj.save()
            return route_task_assignment_obj