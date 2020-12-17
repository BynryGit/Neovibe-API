from rest_framework import serializers
from v1.meter_data_management.models.meter import Meter


class MeterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meter
        fields = ('id_string', 'meter_make')