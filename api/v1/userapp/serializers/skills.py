__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.skills import Skills
from v1.commonapp.serializers.service_type import ServiceTypeSerializer
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.utility.serializers.utility import UtilitySerializer


class SkillListSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    service_type = ServiceTypeSerializer(many=False, required=True, source='get_service_type')

    class Meta:
        model = Skills
        fields = ('id_string', 'tenant', 'utility', 'service_type', 'skill', 'description', 'is_active', 'created_by',
                  'created_date')