__author__ = "aki"

from rest_framework import serializers
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

    class Meta:
        model = BillCycleTbl
        fields = ('id_string', 'code', 'tenant', 'utility')