__author__ = "aki"

from rest_framework import serializers, status
from v1.meter_data_management.models.read_cycle import ReadCycle as ReadCycleTbl


class ReadCycleShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadCycleTbl
        fields = ('id_string','label')
