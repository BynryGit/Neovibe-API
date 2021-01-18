from rest_framework import serializers

from v1.consumer.serializers.service_sub_type import ServiceSubTypeListSerializer
from v1.service.models.consumer_service_master import ConsumerServiceMaster


class ConsumerServiceMasterListSerializer(serializers.ModelSerializer):
    service_sub_type = ServiceSubTypeListSerializer(source='get_service_sub_type')

    class Meta:
        model = ConsumerServiceMaster
        fields = ('id_string', 'name', 'service_sub_type')
