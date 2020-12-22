from rest_framework import serializers
from v1.consumer.serializers.consumer_category import ConsumerCategoryViewSerializer
from v1.consumer.serializers.consumer_sub_category import ConsumerSubCategoryViewSerializer
from v1.utility.models.utility_service_contract_master import UtilityServiceContractMaster
from v1.utility.serializers.utility_service import UtilityServiceListSerializer


class UtilityServiceContractMasterListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    tenant_id_string = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    utility_service = UtilityServiceListSerializer(source='get_service')
    category = ConsumerCategoryViewSerializer(many=False, source='get_consumer_category')
    sub_category = ConsumerSubCategoryViewSerializer(many=False, source='get_consumer_sub_category')

    class Meta:
        model = UtilityServiceContractMaster
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'tenant_id_string', 'utility_id_string', 'utility_service',
                  'category', 'sub_category')


class UtilityServiceContractMasterDetailSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    tenant_id_string = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    utility_service = UtilityServiceListSerializer(source='get_service')
    category = ConsumerCategoryViewSerializer(many=False, source='get_consumer_category')
    sub_category = ConsumerSubCategoryViewSerializer(many=False, source='get_consumer_sub_category')

    class Meta:
        model = UtilityServiceContractMaster
        fields = ('id_string', 'tenant', 'tenant_id_string', 'tenant_id_string', 'utility_id_string', 'utility_service',
                  'category', 'sub_category', 'deposite_amount')
