__author__ = "Gauri"

from django.db import transaction
from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.tenant.models.tenant_summary_on_monthly_basis import TenantSummaryOnMonthlyBasis as TenantUsageSummaryTbl

class TenantUsageSummaryViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)

    class Meta:
        model = TenantUsageSummaryTbl
        fields = ('id_string', 'tenant', 'no_of_utilities','no_of_users','no_of_consumers',
                  'total_no_of_transaction','no_of_cities','no_of_documents','total_storage_in_use','month')