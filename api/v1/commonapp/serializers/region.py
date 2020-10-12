__author__ = "aki"

from rest_framework import serializers
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl


class TenantRegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantRegionTbl
        fields = ('__all__')