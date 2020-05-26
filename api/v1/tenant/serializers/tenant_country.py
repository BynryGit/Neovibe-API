__author__ = "aki"

from rest_framework import serializers
from v1.tenant.models.tenant_country import TenantCountry as TenantCountryTbl


class TenantCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantCountryTbl
        fields = ('id_string', 'name')