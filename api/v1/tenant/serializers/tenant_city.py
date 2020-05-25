from rest_framework import serializers

from v1.tenant.models.tenant_city import TenantCity as TenantCityTbl


class TenantCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantCityTbl
        fields = ('id_string', 'name')