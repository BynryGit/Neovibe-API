from rest_framework import serializers
from v1.commonapp.serializers.service_request_sub_type import ServiceSubTypeListSerializer
from v1.utility.models.utility_service_request_sub_type import UtilityServiceRequestSubType
from v1.utility.serializers.utility_service_request_type import UtilityServiceRequestTypeListSerializer


class UtilityServiceRequestSubTypeListSerializer(serializers.ModelSerializer):
    utility_service_request_type = UtilityServiceRequestTypeListSerializer(source='get_utility_service_request_type')
    service_request_sub_type = ServiceSubTypeListSerializer(source='get_service_request_sub_type')

    class Meta:
        model = UtilityServiceRequestSubType
        fields = ('id_string', 'label', 'utility_service_request_type', 'service_request_sub_type')
