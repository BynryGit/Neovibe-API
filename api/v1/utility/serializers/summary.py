__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_usage_summary import UtilityUsageSummary as UtilityUsageSummaryTbl


class UtilityUsageSummaryViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)

    class Meta:
        model = UtilityUsageSummaryTbl
        fields = ('id_string', 'no_of_users', 'no_of_consumers', 'total_no_of_transaction', 'no_of_cities',
                  'no_of_documents', 'total_storage_in_use', 'month', 'tenant', 'utility',)
