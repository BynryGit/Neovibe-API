__author__ = "aki"

from rest_framework import serializers
from v1.tenant.models.tenant_status import TenantStatus as TenantStatusTbl


class TenantStatusViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantStatusTbl
        fields = ('id_string', 'name')