__author__ = "aki"

from rest_framework import serializers
from v1.meter_reading.models.reading_taken_by import ReadingTakenBy as ReadingTakenByTbl


class ReadingTakenByShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadingTakenByTbl
        fields = ('id_string', 'name')
