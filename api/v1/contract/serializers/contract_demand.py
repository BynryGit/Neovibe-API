__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.contract_demand import ContractDemand as ContractDemandTbl
from v1.contract.serializers.contract import ContractListSerializer
from v1.contract.views.common_functions import set_contract_demand_validated_data


class ContractDemandViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    contract = ContractListSerializer(many=False, required=False, source='get_contract')
    due_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    demand_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ContractDemandTbl
        fields = ('id_string', 'requested_quantity', 'unit', 'actual_quantity', 'rate', 'remark', 'gate_pass_id',
                  'demand_date', 'due_date', 'created_date', 'updated_date', 'tenant', 'utility', 'contract',
                  'supplier_product', 'status_id')


class ContractDemandSerializer(serializers.ModelSerializer):
    supplier_product = serializers.UUIDField(required=False)
    status_id = serializers.UUIDField(required=False)
    requested_quantity = serializers.IntegerField(required=False)
    unit = serializers.IntegerField(required=True)
    actual_quantity = serializers.IntegerField(required=True)
    rate = serializers.FloatField(required=True)
    remark = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = ContractDemandTbl
        fields = ('__all__')

    def create(self, validated_data, contract_obj, user):
        validated_data = set_contract_demand_validated_data(validated_data)
        if ContractDemandTbl.objects.filter(tenant=user.tenant, utility=user.utility,
                                             contract=contract_obj.id, remark=validated_data["remark"]).exists():
            return False
        with transaction.atomic():
            contract_demand_obj = super(ContractDemandSerializer, self).create(validated_data)
            contract_demand_obj.tenant = user.tenant
            contract_demand_obj.utility = user.utility
            contract_demand_obj.contract = contract_obj.id
            contract_demand_obj.created_by = user.id
            contract_demand_obj.save()
            return contract_demand_obj

    def update(self, instance, validated_data, user):
        validated_data = set_contract_demand_validated_data(validated_data)
        with transaction.atomic():
            contract_demand_obj = super(ContractDemandSerializer, self).update(instance, validated_data)
            contract_demand_obj.tenant = user.tenant
            contract_demand_obj.utility = user.utility
            contract_demand_obj.updated_by = user.id
            contract_demand_obj.updated_date = timezone.now()
            contract_demand_obj.save()
            return contract_demand_obj