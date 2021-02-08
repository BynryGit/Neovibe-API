from rest_framework import serializers
from v1.commonapp.serializers.service_request_type import ServiceTypeListSerializer
from v1.utility.models.utility_service_request_type import UtilityServiceRequestType


class UtilityServiceRequestTypeListSerializer(serializers.ModelSerializer):
    service_request_type = ServiceTypeListSerializer(source='get_service_request_type')

    class Meta:
        model = UtilityServiceRequestType
        fields = ('id_string', 'label', 'service_request_type')
