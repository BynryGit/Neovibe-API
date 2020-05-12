from rest_framework import serializers
from v1.consumer.models.consumer_master import ConsumerMaster


class ConsumerViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerMaster
        fields = ('id_string', 'tenant__name', 'tenant__id_string', 'utility__name', 'utility__id_string')