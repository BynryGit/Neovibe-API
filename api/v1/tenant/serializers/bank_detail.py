__author__ = "Gauri"

from rest_framework import serializers

from v1.tenant.serializers.tenant import TenantSerializer
from v1.tenant.models.tenant_bank_details import TenantBankDetails
from v1.tenant.serializers.tenant import TenantSerializer


class BankListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')

    class Meta:
        model = TenantSerializer
        fields = ('id_string', 'tenant','bank_name','branch_name','branch_city','account_number',
                  'account_type','account_name', 'ifsc_no','pan_no','gst_no','tax_id_no','is_active','created_by',
                  'created_date')

class BankViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')


    class Meta:
        model = TenantSerializer
        fields = ('id_string', 'tenant', 'bank_name', 'branch_name', 'branch_city', 'account_number',
                  'account_type', 'account_name', 'ifsc_no', 'pan_no', 'gst_no', 'tax_id_no', 'is_active', 'created_by',
                  'created_date')
