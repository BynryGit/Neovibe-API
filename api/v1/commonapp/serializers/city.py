from rest_framework import serializers

from v1.commonapp.models.city import City
from v1.tenant.models.tenant_city import TenantCity as TenantCityTbl


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantCityTbl
        fields = ('id_string', 'city')