__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.contracts import Contract as ContractTbl
from v1.supplier.views.common_functions import set_supplier_contract_validated_data


class ContractViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)

    class Meta:
        model = ContractTbl
        fields = ('__all__')


class ContractSerializer(serializers.ModelSerializer):
    tenant = serializers.UUIDField(required=True, source='tenant')
    utility = serializers.UUIDField(required=True, source='utility')
    supplier = serializers.IntegerField(required=False)

    class Meta:
        model = ContractTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_supplier_contract_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(ContractSerializer, self).create(validated_data)
            utility_obj.created_by = user.id
            utility_obj.save()
            return utility_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_contract_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(ContractSerializer, self).update(instance, validated_data)
            utility_obj.updated_by = user.id
            utility_obj.updated_date = timezone.now()
            utility_obj.save()
            return utility_obj