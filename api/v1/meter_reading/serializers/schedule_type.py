from rest_framework import serializers
from v1.meter_reading.models.schedule_type import ScheduleType


class ScheduleTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleType
        fields = ('id_string','name')