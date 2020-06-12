__author__ = "aki"

from rest_framework import serializers
from v1.meter_reading.models.schedule_status import ScheduleStatus as ScheduleStatusTbl


class ScheduleStatusShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleStatusTbl
        fields = ('id_string', 'name')