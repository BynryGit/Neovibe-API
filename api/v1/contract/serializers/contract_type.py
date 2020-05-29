__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.contract_type import ContractType as ContractTypeTbl


class ContractTypeShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractTypeTbl
        fields = ('id_string', 'name',)


class ContractTypeViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()

    class Meta:
        model = ContractTypeTbl
        fields = ('id_string', 'name', 'tenant', 'utility')