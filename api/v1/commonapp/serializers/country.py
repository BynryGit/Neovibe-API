__author__ = "aki"

from rest_framework import serializers
from v1.tenant.models.tenant_country import Country as CountryTbl


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = CountryTbl
        fields = ('id_string', 'country')