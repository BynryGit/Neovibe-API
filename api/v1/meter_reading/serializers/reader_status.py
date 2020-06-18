__author__ = "aki"

from rest_framework import serializers
from v1.meter_reading.models.reader_status import ReaderStatus as ReaderStatusTbl


class ReaderStatusShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReaderStatusTbl
        fields = ('id_string', 'name')
