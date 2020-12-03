from rest_framework import serializers
from v1.utility.models.utility_service_contract_master import UtilityServiceContractMaster


class UtilityServiceContractMasterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityServiceContractMaster
        fields = '__all__'
