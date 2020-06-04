from rest_framework import serializers
from v1.meter_reading.models.schedule_status import ScheduleStatus


class ScheduleStatusListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleStatus
        fields = ('id_string','name')