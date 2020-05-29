__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.contract_period import ContractPeriod as ContractPeriodTbl


class ContractPeriodShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractPeriodTbl
        fields = ('id_string', 'period',)


class ContractPeriodViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()

    class Meta:
        model = ContractPeriodTbl
        fields = ('id_string', 'period', 'tenant', 'utility')