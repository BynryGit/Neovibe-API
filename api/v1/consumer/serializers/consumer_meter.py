from rest_framework import serializers
from v1.consumer.models.consumer_meter import ConsumerMeter


class ConsumerMeterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerMeter
        fields = '__all__'

