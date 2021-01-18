from rest_framework import serializers

from v1.service.models.consumer_service_master import ConsumerServiceMaster


class ConsumerServiceMasterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerServiceMaster
        fields = ('id_string', 'name', )
