__author__ = "aki"

from rest_framework import serializers
from v1.tenant.models.tenant_master import TenantMaster as TenantMasterTbl


class TenantMasterViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantMasterTbl
        fields = ('id_string', 'name', 'short_name')