from rest_framework import serializers, status
from v1.consumer.serializers.consumer_category import ConsumerCategoryViewSerializer
from v1.consumer.serializers.consumer_sub_category import ConsumerSubCategoryViewSerializer
from v1.utility.models.utility_service_contract_master import UtilityServiceContractMaster
from v1.utility.serializers.utility_service import UtilityServiceListSerializer
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.views.common_functions import set_utility_contract_validated_data
from api.messages import CONTRACT_ALREADY_EXIST


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
        fields = (
            'id_string', 'deposite_amount', 'name', 'tenant', 'tenant_id_string', 'tenant_id_string',
            'utility_id_string',
            'utility_service',
            'category', 'sub_category','start_date', 'end_date')


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
        fields = ('name', 'id_string', 'tenant', 'tenant_id_string', 'tenant_id_string', 'utility_id_string', 'utility_service',
                  'category', 'sub_category','terms', 'deposite_amount','start_date', 'end_date')


class UtilityServiceContractMasterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityServiceContractMaster
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string', 'start_date', 'end_date')


class UtilityServiceContractMasterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    service_id = serializers.CharField(required=False, max_length=200)
    consumer_category_id = serializers.CharField(required=False, max_length=200)
    consumer_sub_category_id = serializers.CharField(required=False, max_length=200)
    service_contract_template_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityServiceContractMaster
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_utility_contract_validated_data(validated_data)
            if UtilityServiceContractMaster.objects.filter(name=validated_data['name'],
                                                           tenant_id=validated_data['tenant_id'],
                                                           utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(CONTRACT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                contract_obj = super(UtilityServiceContractMasterSerializer, self).create(validated_data)
                contract_obj.created_by = user.id
                contract_obj.updated_by = user.id
                contract_obj.save()
                return contract_obj

    def update(self, instance, validated_data, user):
        validated_data = set_utility_contract_validated_data(validated_data)
        with transaction.atomic():
            contract_obj = super(UtilityServiceContractMasterSerializer, self).update(instance, validated_data)
            contract_obj.updated_by = user.id
            contract_obj.updated_date = datetime.utcnow()
            contract_obj.save()
            return contract_obj
