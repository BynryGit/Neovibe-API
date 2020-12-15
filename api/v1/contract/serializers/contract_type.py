__author__ = "Gaurav"

from rest_framework import serializers, status
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.contract_type import ContractType as ContractTypeTbl
from v1.contract.views.common_functions import set_contract_validated_data
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NAME_ALREADY_EXIST




class ContractTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractTypeTbl
        fields = ('id_string', 'name','is_active','created_by','created_date')


class ContractTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ContractTypeTbl
        fields = ('id_string', 'name', 'tenant','tenant_id_string','utility','utility_id_string')

class ContractTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ContractTypeTbl
        fields = ('__all__')

    def create(self, validated_data,  user):
        with transaction.atomic():
            validated_data = set_contract_validated_data(validated_data)
            if ContractTypeTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                contract_type_obj = super(ContractTypeSerializer, self).create(validated_data)
                contract_type_obj.created_by = user.id
                contract_type_obj.updated_by = user.id
                contract_type_obj.save()
                return contract_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_contract_validated_data(validated_data)
        if ContractTypeTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                contract_type_obj = super(ContractTypeSerializer, self).update(instance, validated_data)
                contract_type_obj.updated_by = user.id
                contract_type_obj.updated_date = datetime.utcnow()
                contract_type_obj.save()
                return contract_type_obj