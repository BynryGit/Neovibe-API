__author__ = "aki"

from rest_framework import serializers
from v1.meter_reading.models.activity_type import ActivityType as ActivityTypeTbl


class ActivityTypeShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityTypeTbl
        fields = ('id_string', 'name')