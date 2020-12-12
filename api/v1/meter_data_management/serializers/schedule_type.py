__author__ = "aki"

from rest_framework import serializers
from v1.meter_data_management.models.schedule_type import ScheduleType as ScheduleTypeTbl


class ScheduleTypeShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleTypeTbl
        fields = ('id_string', 'name')