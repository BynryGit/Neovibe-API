__author__ = "aki"

from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.jobcard import Jobcard as JobcardTbl
from v1.meter_data_management.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.serializers.route_assignment import RouteAssignmentShortViewSerializer
from v1.userapp.serializers.user import UserViewSerializer


class JobcardShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobcardTbl
        fields = ('id_string', 'consumer_no')


class JobcardViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    bill_cycle_id = BillCycleShortViewSerializer(many=False, required=False, source='get_bill_cycle')
    route_id = RouteShortViewSerializer(many=False, required=False, source='get_route')
    route_assigned_id = RouteAssignmentShortViewSerializer(many=False, required=False,
                                                         source='get_route_assignment')
    meter_reader_id = UserViewSerializer(many=False, required=False, source='get_meter_reader')
    assign_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    completion_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = JobcardTbl
        fields = ('id_string', 'consumer_no', 'month', 'assign_date', 'completion_date', 'created_date', 'updated_date',
                  'bill_cycle_id', 'route_id', 'route_assigned_id', 'meter_reader_id', 'tenant', 'utility')