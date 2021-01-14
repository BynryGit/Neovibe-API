__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.contract import Contract as ContractTbl
from v1.supplier.serializers.supplier import SupplierShortViewSerializer
from v1.supplier.views.common_functions import set_supplier_contract_validated_data


class ContractViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    supplier = SupplierShortViewSerializer(many=False, required=False, source='get_supplier')
    start_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    end_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ContractTbl
        fields = ('id_string', 'name', 'description', 'contract_amount', 'start_date', 'end_date', 'created_date',
                  'updated_date', 'tenant', 'utility', 'contract_type', 'contract_period', 'supplier',
                  'supplier_product_id', 'cost_center', 'status')


class ContractSerializer(serializers.ModelSerializer):
    contract_type = serializers.UUIDField(required=False)
    contract_period = serializers.UUIDField(required=False)
    status = serializers.UUIDField(required=False)
    cost_center = serializers.UUIDField(required=False)
    supplier_product_id = serializers.UUIDField(required=False)
    name = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = ContractTbl
        fields = ('__all__')

    def create(self, validated_data, supplier_obj, user):
        validated_data = set_supplier_contract_validated_data(validated_data)
        if ContractTbl.objects.filter(tenant=user.tenant, utility=user.utility,
                                             supplier=supplier_obj.id, name=validated_data["name"]).exists():
            return False
        with transaction.atomic():
            supplier_contract_obj = super(ContractSerializer, self).create(validated_data)
            supplier_contract_obj.tenant = user.tenant
            supplier_contract_obj.utility = user.utility
            supplier_contract_obj.supplier = supplier_obj.id
            supplier_contract_obj.created_by = user.id
            supplier_contract_obj.save()
            return supplier_contract_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_contract_validated_data(validated_data)
        with transaction.atomic():
            supplier_contract_obj = super(ContractSerializer, self).update(instance, validated_data)
            supplier_contract_obj.tenant = user.tenant
            supplier_contract_obj.utility = user.utility
            supplier_contract_obj.updated_by = user.id
            supplier_contract_obj.updated_date = timezone.now()
            supplier_contract_obj.save()
            return supplier_contract_obj