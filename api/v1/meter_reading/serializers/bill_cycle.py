__author__ = "aki"

from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_reading.models.bill_cycle import BillCycle as BillCycleTbl


class BillCycleShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillCycleTbl
        fields = ('id_string', 'code')


class BillCycleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = BillCycleTbl
        fields = ('id_string', 'code', 'created_date', 'updated_date', 'tenant', 'utility')