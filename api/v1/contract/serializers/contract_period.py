__author__ = "aki"

from rest_framework import serializers, status
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.contract_period import ContractPeriod as ContractPeriodTbl
from v1.contract.views.common_functions import set_contract_validated_data
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NAME_ALREADY_EXIST

class ContractPeriodListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractPeriodTbl
        fields = ('id_string', 'period','is_active','created_by','created_date')


# class ContractPeriodViewSerializer(serializers.ModelSerializer):
#     tenant = TenantMasterViewSerializer()
#     utility = UtilityMasterViewSerializer()

#     class Meta:
#         model = ContractPeriodTbl
#         fields = ('id_string', 'period', 'tenant', 'utility')

class ContractPeriodViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ContractPeriodTbl
        fields = ('id_string', 'period', 'tenant','tenant_id_string','utility','utility_id_string')

class ContractPeriodSerializer(serializers.ModelSerializer):
    period = serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ContractPeriodTbl
        fields = ('__all__')

    def create(self, validated_data,  user):
        with transaction.atomic():
            validated_data = set_contract_validated_data(validated_data)
            if ContractPeriodTbl.objects.filter(period=validated_data['period'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                contract_period_obj = super(ContractPeriodSerializer, self).create(validated_data)
                contract_period_obj.created_by = user.id
                contract_period_obj.updated_by = user.id
                contract_period_obj.save()
                return contract_period_obj

    def update(self, instance, validated_data, user):
        validated_data = set_contract_validated_data(validated_data)
        if ContractPeriodTbl.objects.filter(period=validated_data['period'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                contract_period_obj = super(ContractPeriodSerializer, self).update(instance, validated_data)
                contract_period_obj.updated_by = user.id
                contract_period_obj.updated_date = datetime.utcnow()
                contract_period_obj.save()
                return contract_period_obj