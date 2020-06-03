from rest_framework import serializers
from v1.tenant.models.tenant_status import TenantStatus as TenantStatusTbl


class TenantStatusShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantStatusTbl
        fields = ('id_string', 'name')