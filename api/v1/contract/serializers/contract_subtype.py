__author__ = "Gaurav"

from rest_framework import serializers, status
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.contract_subtype import ContractSubType as ContractSubTypeTbl
from v1.contract.views.common_functions import set_contract_validated_data
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.contract.serializers.contract_type import ContractTypeListSerializer
from api.messages import NAME_ALREADY_EXIST



class ContractSubTypeListSerializer(serializers.ModelSerializer):
    contract_type=ContractTypeListSerializer(many=False, source='get_contract_type')

    class Meta:
        model = ContractSubTypeTbl
        fields = ('id_string', 'name','is_active','created_by','created_date','contract_type')

class ContractSubTypeViewSerializer(serializers.ModelSerializer):
    contract_type=ContractTypeListSerializer(many=False, source='get_contract_type')
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ContractSubTypeTbl
        fields = ('id_string', 'name', 'tenant','tenant_id_string','utility','utility_id_string','contract_type')

class ContractSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    type_id=serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ContractSubTypeTbl
        fields = ('__all__')

    def create(self, validated_data,  user):
        with transaction.atomic():
            validated_data = set_contract_validated_data(validated_data)
            if ContractSubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                contract_subtype_obj = super(ContractSubTypeSerializer, self).create(validated_data)
                contract_subtype_obj.created_by = user.id
                contract_subtype_obj.updated_by = user.id
                contract_subtype_obj.save()
                return contract_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_contract_validated_data(validated_data)
        if ContractSubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                contract_subtype_obj = super(ContractSubTypeSerializer, self).update(instance, validated_data)
                contract_subtype_obj.updated_by = user.id
                contract_subtype_obj.updated_date = datetime.utcnow()
                contract_subtype_obj.save()
                return contract_subtype_obj