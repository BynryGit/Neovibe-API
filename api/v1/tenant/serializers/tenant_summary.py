__author__ = "aki"

from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.tenant.models.tenant_summary_on_monthly_basis import TenantSummaryOnMonthlyBasis as TenantSummaryOnMonthlyBasisTbl


class TenantSummaryOnMonthlyBasisViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TenantSummaryOnMonthlyBasisTbl
        fields = ('id_string', 'no_of_utilities', 'no_of_users', 'no_of_consumers', 'total_no_of_transaction',
                  'no_of_cities', 'no_of_documents', 'total_storage_in_use', 'month', 'created_date', 'updated_date',
                  'tenant')