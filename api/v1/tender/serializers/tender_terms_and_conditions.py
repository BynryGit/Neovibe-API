__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.tender.models.tender_terms_and_conditions import TenderTermsAndCondition as TenderTermsAndConditionTbl
from v1.tender.serializers.tender import TenderShortViewSerializer


class TenderTermsAndConditionViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    tender = TenderShortViewSerializer(many=False, required=False, source='get_tender')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TenderTermsAndConditionTbl
        fields = ('id_string', 'terms_name', 'terms', 'created_date', 'updated_date', 'tender', 'tenant', 'utility')


class TenderTermsAndConditionSerializer(serializers.ModelSerializer):
    terms_name = serializers.CharField(required=True, max_length=200)
    terms = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = TenderTermsAndConditionTbl
        fields = ('__all__')

    def create(self, validated_data, tender_obj, user):
        if TenderTermsAndConditionTbl.objects.filter(tenant=user.tenant, utility_id=1, tender_id=tender_obj.id,
                                                     terms_name=validated_data["terms_name"]).exists():
            return False
        with transaction.atomic():
            tender_term_and_condition_obj = super(TenderTermsAndConditionSerializer, self).create(validated_data)
            tender_term_and_condition_obj.tenant = user.tenant
            tender_term_and_condition_obj.utility_id = 1
            tender_term_and_condition_obj.tender_id = tender_obj.id
            tender_term_and_condition_obj.created_by = user.id
            tender_term_and_condition_obj.save()
            return tender_term_and_condition_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            tender_term_and_condition_obj = super(TenderTermsAndConditionSerializer, self).update(instance, validated_data)
            tender_term_and_condition_obj.tenant = user.tenant
            tender_term_and_condition_obj.utility_id = 1
            tender_term_and_condition_obj.updated_by = user.id
            tender_term_and_condition_obj.updated_date = timezone.now()
            tender_term_and_condition_obj.save()
            return tender_term_and_condition_obj
