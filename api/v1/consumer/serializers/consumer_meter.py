from rest_framework import serializers
from v1.consumer.models.consumer_meter import ConsumerMeter
from v1.meter_data_management.serializers.meter import MeterListSerializer


class ConsumerMeterListSerializer(serializers.ModelSerializer):
    meter = MeterListSerializer(source='get_meter')

    class Meta:
        model = ConsumerMeter
        fields = ('id_string', 'meter')

