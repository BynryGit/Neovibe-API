from rest_framework import serializers
from v1.meter_reading.models.activity_type import ActivityType


class ActivityTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityType
        fields = ('id_string','name')