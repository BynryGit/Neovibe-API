__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.contract import Contract as ContractTbl
from v1.contract.serializers.contract_period import ContractPeriodListSerializer
from v1.contract.serializers.contract_status import ContractStatusShortViewSerializer
from v1.contract.serializers.contract_type import ContractTypeListSerializer
from v1.contract.views.common_functions import set_contract_validated_data


class ContractListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractTbl
        fields = ('id_string', 'name')


class ContractViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    contract_type = ContractTypeListSerializer(many=False, required=False, source='get_contract_type')
    contract_period = ContractPeriodListSerializer(many=False, required=False, source='get_contract_period')
    # status = ContractStatusShortViewSerializer(many=False, required=False, source='get_contract_status')
    start_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    end_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ContractTbl
        fields = ('id_string', 'name', 'description', 'contract_amount', 'start_date', 'end_date', 'created_date',
                  'updated_date', 'tenant', 'utility', 'contract_type', 'contract_period', 'status', 'cost_center')


class ContractSerializer(serializers.ModelSerializer):
    contract_type = serializers.UUIDField(required=True)
    contract_period = serializers.UUIDField(required=True)
    status = serializers.UUIDField(required=False)
    cost_center = serializers.UUIDField(required=False)
    name = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = ContractTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_contract_validated_data(validated_data)
        if ContractTbl.objects.filter(tenant=user.tenant, utility=user.utility, name=validated_data["name"]).exists():
            return False
        with transaction.atomic():
            contract_obj = super(ContractSerializer, self).create(validated_data)
            contract_obj.tenant = user.tenant
            contract_obj.utility = user.utility
            contract_obj.created_by = user.id
            contract_obj.save()
            return contract_obj

    def update(self, instance, validated_data, user):
        validated_data = set_contract_validated_data(validated_data)
        with transaction.atomic():
            contract_obj = super(ContractSerializer, self).update(instance, validated_data)
            contract_obj.tenant = user.tenant
            contract_obj.utility = user.utility
            contract_obj.updated_by = user.id
            contract_obj.updated_date = timezone.now()
            contract_obj.save()
            return contract_obj