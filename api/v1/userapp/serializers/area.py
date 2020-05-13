__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.skills import Skills
from v1.commonapp.serializers.city import CitySerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.utility.serializers.utility import UtilitySerializer


class AreaListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    city = CitySerializer(many=False, required=True, source='get_city')

    class Meta:
        model = Skills
        fields = ('id_string', 'tenant', 'utility', 'city', 'name', 'is_active', 'created_by',
                  'created_date')