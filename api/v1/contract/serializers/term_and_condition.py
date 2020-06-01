__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.models.terms_and_conditions import TermsAndCondition as TermsAndConditionTbl
from v1.contract.serializers.contract import ContractShortViewSerializer


class TermsAndConditionViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    contract = ContractShortViewSerializer(many=False, required=False, source='get_contract')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TermsAndConditionTbl
        fields = ('id_string', 'terms_name', 'terms', 'created_date', 'updated_date', 'tenant', 'utility', 'contract')


class TermsAndConditionSerializer(serializers.ModelSerializer):
    terms_name = serializers.CharField(required=True, max_length=200)
    terms = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = TermsAndConditionTbl
        fields = ('__all__')

    def create(self, validated_data, contract_obj, user):
        if TermsAndConditionTbl.objects.filter(tenant=user.tenant, utility=user.utility, contract=contract_obj.id,
                                               terms_name=validated_data["terms_name"]).exists():
            return False
        with transaction.atomic():
            contract_term_and_condition_obj = super(TermsAndConditionSerializer, self).create(validated_data)
            contract_term_and_condition_obj.tenant = user.tenant
            contract_term_and_condition_obj.utility = user.utility
            contract_term_and_condition_obj.contract = contract_obj.id
            contract_term_and_condition_obj.created_by = user.id
            contract_term_and_condition_obj.save()
            return contract_term_and_condition_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            contract_term_and_condition_obj = super(TermsAndConditionSerializer, self).update(instance, validated_data)
            contract_term_and_condition_obj.tenant = user.tenant
            contract_term_and_condition_obj.utility = user.utility
            contract_term_and_condition_obj.updated_by = user.id
            contract_term_and_condition_obj.updated_date = timezone.now()
            contract_term_and_condition_obj.save()
            return contract_term_and_condition_obj