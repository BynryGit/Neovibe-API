__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.tender.models.tender_quotation import TenderQuotation as TenderQuotationTbl
from v1.tender.serializers.tender import TenderShortViewSerializer
from v1.tender.serializers.tender_vendor import TenderVendorShortViewSerializer
from v1.tender.views.common_functions import set_tender_quotation_validated_data


class TenderQuotationViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    tender_id = TenderShortViewSerializer(many=False, required=False, source='get_tender')
    vendor_id = TenderVendorShortViewSerializer(many=False, required=False, source='get_vendor')
    submission_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = TenderQuotationTbl
        fields = ('id_string', 'amount', 'description', 'submission_date', 'created_date', 'updated_date', 'tender_id',
                  'vendor_id', 'tenant', 'utility')


class TenderQuotationSerializer(serializers.ModelSerializer):
    vendor_id = serializers.UUIDField(required=False)
    amount = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = TenderQuotationTbl
        fields = ('__all__')

    def create(self, validated_data, tender_obj, user):
        validated_data = set_tender_quotation_validated_data(validated_data)
        if TenderQuotationTbl.objects.filter(tenant=user.tenant, utility_id=1,
                                             tender_id=tender_obj.id, amount=validated_data["amount"]).exists():
            return False
        with transaction.atomic():
            tender_quotation_obj = super(TenderQuotationSerializer, self).create(validated_data)
            tender_quotation_obj.tenant = user.tenant
            tender_quotation_obj.utility_id = 1
            tender_quotation_obj.tender_id = tender_obj.id
            tender_quotation_obj.created_by = user.id
            tender_quotation_obj.save()
            return tender_quotation_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tender_quotation_validated_data(validated_data)
        with transaction.atomic():
            tender_quotation_obj = super(TenderQuotationSerializer, self).update(instance, validated_data)
            tender_quotation_obj.tenant = user.tenant
            tender_quotation_obj.utility_id = 1
            tender_quotation_obj.updated_by = user.id
            tender_quotation_obj.updated_date = timezone.now()
            tender_quotation_obj.save()
            return tender_quotation_obj
