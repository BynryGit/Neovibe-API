from rest_framework import serializers

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.models.skills import Skills
from v1.commonapp.serializers.service_type import GetServiceTypeSerializer
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.utility.serializers.utility import UtilitySerializer


class GetSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = ('skill', 'id_string')


class SkillViewSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    service_type = GetServiceTypeSerializer(many=False, required=True, source='get_service_type')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = Skills
        fields = ('id_string', 'skill', 'description', 'created_date', 'updated_date', 'tenant', 'utility', 'service_type')