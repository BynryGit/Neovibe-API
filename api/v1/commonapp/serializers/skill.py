from rest_framework import serializers

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.models.skills import Skills
from v1.commonapp.serializers.service_type import GetServiceTypeSerializer
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.utility.serializers.utility import UtilitySerializer


class GetSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = ('skill', 'id_string')


class SkillViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    service_type = GetServiceTypeSerializer(many=False, required=True, source='get_service_type')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = Skills
        fields = ('id_string', 'skill', 'description', 'tenant', 'utility', 'service_type', 'created_date')