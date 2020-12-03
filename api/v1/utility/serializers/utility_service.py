from rest_framework import serializers

from v1.utility.models.utility_service import UtilityService
from v1.utility.serializers.utility_service_master import UtilityServiceMasterListSerializer


class UtilityServiceListSerializer(serializers.ModelSerializer):
    service = UtilityServiceMasterListSerializer(many=False, source='get_service')

    class Meta:
        model = UtilityService
        fields = ('id_string', 'service')