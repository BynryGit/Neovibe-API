__author__ = "Arpita"

from rest_framework import serializers

from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.models.user_bank_detail import UserBankDetails
from v1.utility.serializers.utility import UtilitySerializer


class BankListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = UserBankDetails
        fields = ('id_string', 'tenant', 'utility', 'bank_name', 'branch_name', 'branch_city', 'account_number',
                  'account_type', 'account_name', 'ifsc_no', 'pan_no', 'gst_no', 'tax_id_no', 'is_active', 'created_by',
                  'created_date')


class BankViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = UserBankDetails
        fields = ('id_string', 'tenant', 'utility', 'bank_name', 'branch_name', 'branch_city', 'account_number',
                  'account_type', 'account_name', 'ifsc_no', 'pan_no', 'gst_no', 'tax_id_no', 'is_active', 'created_by',
                  'created_date')
