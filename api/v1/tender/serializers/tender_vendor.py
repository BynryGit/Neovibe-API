__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.tender.models.tender_vendor import TenderVendor as TenderVendorTbl
from v1.tender.serializers.tender import TenderShortViewSerializer
from v1.tender.views.common_functions import set_tender_vendor_validated_data
from v1.userapp.serializers.user import GetUserSerializer


class TenderVendorShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenderVendorTbl
        fields = ('id_string',)


class TenderVendorViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    tender_id = TenderShortViewSerializer(many=False, required=False, source='get_tender')
    vendor_id = GetUserSerializer(many=False, required=False, source='get_vendor')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = TenderVendorTbl
        fields = ('id_string', 'created_date', 'updated_date', 'tender_id', 'vendor_id', 'tenant', 'utility')


class TenderVendorSerializer(serializers.ModelSerializer):
    vendor_id = serializers.UUIDField(required=True)

    class Meta:
        model = TenderVendorTbl
        fields = ('__all__')

    def create(self, validated_data, tender_obj, user):
        validated_data = set_tender_vendor_validated_data(validated_data)
        if TenderVendorTbl.objects.filter(tenant=user.tenant, utility_id=1, tender_id=tender_obj.id,
                                          vendor_id=validated_data["vendor_id"]).exists():
            return False
        with transaction.atomic():
            tender_vendor_obj = super(TenderVendorSerializer, self).create(validated_data)
            tender_vendor_obj.tenant = user.tenant
            tender_vendor_obj.utility_id = 1
            tender_vendor_obj.tender_id = tender_obj.id
            tender_vendor_obj.created_by = user.id
            tender_vendor_obj.save()
            return tender_vendor_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tender_vendor_validated_data(validated_data)
        with transaction.atomic():
            tender_vendor_obj = super(TenderVendorSerializer, self).update(instance, validated_data)
            tender_vendor_obj.tenant = user.tenant
            tender_vendor_obj.utility_id = 1
            tender_vendor_obj.updated_by = user.id
            tender_vendor_obj.updated_date = timezone.now()
            tender_vendor_obj.save()
            return tender_vendor_obj
