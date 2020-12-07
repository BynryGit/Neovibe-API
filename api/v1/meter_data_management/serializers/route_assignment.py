__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.route_assignment import RouteAssignment as RouteAssignmentTbl
from v1.meter_data_management.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.serializers.route_assignment_status import RouteAssignmentStatusShortViewSerializer
from v1.meter_data_management.views.common_functions import set_route_assignment_validated_data
from v1.userapp.serializers.user import UserViewSerializer


class RouteAssignmentShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAssignmentTbl
        fields = ('id_string', 'month')


class RouteAssignmentViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    bill_cycle_id = BillCycleShortViewSerializer(many=False, required=False, source='get_bill_cycle')
    route_id = RouteShortViewSerializer(many=False, required=False, source='get_route')
    status_id = RouteAssignmentStatusShortViewSerializer(many=False, required=False, source='get_route_assignment_status')
    meter_reader_id = UserViewSerializer(many=False, required=False, source='get_meter_reader')
    assign_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = RouteAssignmentTbl
        fields = ('__all__')


class RouteAssignmentSerializer(serializers.ModelSerializer):
    meter_reader_id = serializers.UUIDField(required=True)
    month = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = RouteAssignmentTbl
        fields = ('__all__')

    def create(self, validated_data, route_obj, user):
        validated_data = set_route_assignment_validated_data(validated_data)
        if RouteAssignmentTbl.objects.filter(tenant=user.tenant, utility=1, bill_cycle_id=route_obj.bill_cycle_id,
                                             route_id=route_obj.id, meter_reader_id=validated_data["meter_reader_id"]).exists():
            return False
        with transaction.atomic():
            route_assignment_obj = super(RouteAssignmentSerializer, self).create(validated_data)
            route_assignment_obj.tenant = user.tenant
            route_assignment_obj.utility_id = 1
            route_assignment_obj.bill_cycle_id = route_obj.bill_cycle_id
            route_assignment_obj.route_id = route_obj.id
            route_assignment_obj.created_by = user.id
            route_assignment_obj.save()
            return route_assignment_obj


class RouteDeAssignmentSerializer(serializers.ModelSerializer):
    month = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = RouteAssignmentTbl
        fields = ('__all__')

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            route_assignment_obj = super(RouteAssignmentSerializer, self).update(instance, validated_data)
            route_assignment_obj.tenant = user.tenant
            route_assignment_obj.utility_id = 1
            route_assignment_obj.status_id = 1
            route_assignment_obj.updated_by = user.id
            route_assignment_obj.updated_date = timezone.now()
            route_assignment_obj.save()
            return route_assignment_obj
