__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from api.messages import ACCOUNT_NO_ALREADY_EXIST
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_bank_details import TenantBankDetail as TenantBankDetailTbl


class TenantBankDetailShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantBankDetailTbl
        fields = ('id_string', 'bank_name', 'branch_name', 'branch_city', 'account_number', 'account_type',
                  'account_name')


class TenantBankDetailViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TenantBankDetailTbl
        fields = ('id_string', 'bank_name', 'branch_name', 'branch_city', 'account_number', 'account_type',
                  'account_name', 'ifsc_no', 'pan_no', 'gst_no', 'tax_id_no', 'created_date', 'updated_date', 'tenant')


class TenantBankDetailSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(required=True, max_length=200)
    branch_name = serializers.CharField(required=False, max_length=200)
    branch_city = serializers.CharField(required=False, max_length=200)
    account_number = serializers.CharField(required=True, max_length=200)
    account_type = serializers.CharField(required=False, max_length=200)
    account_name = serializers.CharField(required=True, max_length=200)
    ifsc_no = serializers.CharField(required=False, max_length=200)
    pan_no = serializers.CharField(required=False, max_length=200)
    gst_no = serializers.CharField(required=False, max_length=200)
    tax_id_no = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = TenantBankDetailTbl
        fields = ('__all__')

    def create(self, validated_data, tenant_obj, user):
        if TenantBankDetailTbl.objects.filter(tenant=tenant_obj, account_number=validated_data["account_number"]).exists():
            raise CustomAPIException(ACCOUNT_NO_ALREADY_EXIST,status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            tenant_bank_obj = super(TenantBankDetailSerializer, self).create(validated_data)
            tenant_bank_obj.tenant = tenant_obj
            tenant_bank_obj.created_by = user.id
            tenant_bank_obj.save()
            return tenant_bank_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            tenant_bank_obj = super(TenantBankDetailSerializer, self).update(instance, validated_data)
            tenant_bank_obj.updated_date = timezone.now()
            tenant_bank_obj.save()
            return tenant_bank_obj
