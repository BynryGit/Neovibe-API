__author__ = "aki"

from rest_framework import serializers
from v1.meter_reading.models.meter_image_type import MeterImageType as MeterImageTypeTbl


class MeterImageTypeShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeterImageTypeTbl
        fields = ('id_string', 'name')
