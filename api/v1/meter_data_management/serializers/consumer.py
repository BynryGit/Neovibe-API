__author__ = "aki"

from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.consumer import Consumer as ConsumerTbl
from v1.meter_data_management.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer


class ConsumerShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerTbl
        fields = ('id_string', 'consumer_no')


class ConsumerViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    bill_cycle_id = BillCycleShortViewSerializer(many=False, source='get_bill_cycle')
    route_id = RouteShortViewSerializer(many=False, source='get_route')
    reading_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ConsumerTbl
        fields = ('id_string', 'consumer_no', 'first_name', 'middle_name', 'last_name', 'email_id', 'phone_mobile',
                  'address_line_1', 'bill_month', 'meter_no', 'current_reading', 'reading_date', 'outstanding', 'month',
                  'is_meter_reading', 'is_bill_distribution', 'created_date', 'tenant', 'updated_date', 'utility',
                  'bill_cycle_id', 'route_id')
