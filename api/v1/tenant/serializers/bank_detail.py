__author__ = "Gauri"

from django.db import transaction
from rest_framework import serializers

from v1.tenant.models import tenant_bank_details
from v1.tenant.serializers.tenant import TenantMasterSerializer
from v1.tenant.models.tenant_bank_details import TenantBankDetails
from v1.tenant.serializers.tenant import TenantMasterSerializer
from v1.tenant.views.common_functions import set_validated_data


class BankListSerializer(serializers.ModelSerializer):
    # tenant = TenantSerializer(many=False, required=True, source='get_tenant')

    class Meta:
        model = TenantBankDetails
        fields = ('id_string', 'tenant','bank_name','branch_name','branch_city','account_number',
                  'account_type','account_name', 'ifsc_no','pan_no','gst_no','tax_id_no','is_active','created_by',
                  'created_date')

class BankViewSerializer(serializers.ModelSerializer):
    # tenant = TenantSerializer(many=False, required=True, source='get_tenant')


    class Meta:
        model = TenantBankDetails
        fields = ('id_string', 'tenant', 'bank_name', 'branch_name', 'branch_city', 'account_number',
                  'account_type', 'account_name', 'ifsc_no', 'pan_no', 'gst_no', 'tax_id_no', 'is_active', 'created_by',
                  'created_date')

class TenantBankSerializer(serializers.ModelSerializer):

    id_string = serializers.CharField(required=False, max_length=200)
    tenant = serializers.CharField(required=False, max_length=200)
    bank_name = serializers.CharField(required=False, max_length=200)
    branch_name = serializers.CharField(required=False, max_length=200)
    branch_city = serializers.CharField(required=False, max_length=200)
    account_number = serializers.CharField(required=False, max_length=200)
    account_type = serializers.CharField(required=False, max_length=200)
    account_name = serializers.CharField(required=False, max_length=200)
    ifsc_no = serializers.CharField(required=False, max_length=200)
    pan_no = serializers.CharField(required=False, max_length=200)
    gst_no = serializers.CharField(required=False, max_length=200)
    tax_id_no = serializers.CharField(required=False, max_length=200)
    is_active = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = TenantBankDetails
        fields = ('id_string', 'tenant', 'bank_name', 'branch_name', 'branch_city', 'account_number',
                  'account_type', 'account_name', 'ifsc_no', 'pan_no', 'gst_no', 'tax_id_no', 'is_active', 'created_by',
                  'created_date')

    def create(self, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            tenant_bank_obj = super(TenantBankSerializer, self).create(validated_data)
            # tenant_obj.created_by = user.id
            # tenant_obj.created_date = datetime.utcnow()
            # tenant_obj.tenant = user.tenant
            tenant_bank_obj.save()
            return tenant_bank_obj

    def update(self, instance, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            tenant_bank_obj = super(TenantBankSerializer, self).update(instance, validated_data)
            # tenant_obj.updated_by = user.id
            # tenant_obj.updated_date = datetime.utcnow()
            tenant_bank_obj.save()
            return tenant_bank_obj