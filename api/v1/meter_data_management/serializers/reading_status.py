__author__ = "aki"

from rest_framework import serializers
from v1.meter_data_management.models.reading_status import ReadingStatus as ReadingStatusTbl


class ReadingStatusShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadingStatusTbl
        fields = ('id_string', 'name')
