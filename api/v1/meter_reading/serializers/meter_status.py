__author__ = "aki"

from rest_framework import serializers
from v1.meter_reading.models.meter_status import MeterStatus as MeterStatusTbl


class MeterStatusShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeterStatusTbl
        fields = ('id_string', 'name')
