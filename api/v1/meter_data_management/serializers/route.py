__author__ = "aki"

from rest_framework import serializers
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.route import Route as RouteTbl
from v1.meter_data_management.serializers.bill_cycle import BillCycleShortViewSerializer


class RouteShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteTbl
        fields = ('id_string', 'code', 'token')


class RouteViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    bill_cycle_id = BillCycleShortViewSerializer(many=False, source='get_bill_cycle')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = RouteTbl
        fields = ('id_string', 'code', 'token', 'month', 'is_meter_reading', 'is_bill_distribution', 'created_date',
                  'updated_date', 'bill_cycle_id', 'tenant', 'utility')
