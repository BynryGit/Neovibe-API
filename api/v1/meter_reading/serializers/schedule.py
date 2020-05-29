from rest_framework import serializers
from v1.consumer.models.consumer_master import get_consumers_by_cycle_id
from v1.meter_reading.models.schedule import Schedule
from v1.meter_reading.serializers.activity_type import ActivityTypeListSerializer
from v1.meter_reading.serializers.schedule_type import ScheduleTypeListSerializer


class ScheduleListSerializer(serializers.ModelSerializer):
    schedule_type = ScheduleTypeListSerializer(many=False, source='get_schedule_type')
    activity_type = ActivityTypeListSerializer(many=False, source='get_activity_type')
    consumers = serializers.SerializerMethodField()

    def get_consumers(self,obj):
        consumers = get_consumers_by_cycle_id(obj.bill_cycle_id).count()
        return consumers

    class Meta:
        model = Schedule
        fields = ('schedule_id_string','bill_month','schedule_type','activity_type','consumers')