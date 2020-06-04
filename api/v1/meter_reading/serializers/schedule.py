from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from v1.consumer.models.consumer_master import get_consumers_by_cycle_id
from v1.meter_reading.models.schedule import Schedule
from v1.meter_reading.serializers.activity_type import ActivityTypeListSerializer
from v1.meter_reading.serializers.bill_cycle import BillCycleListSerializer
from v1.meter_reading.serializers.schedule_status import ScheduleStatusListSerializer
from v1.meter_reading.serializers.schedule_type import ScheduleTypeListSerializer
from v1.meter_reading.views.common_functions import set_schedule_validated_data


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


class ScheduleViewSerializer(serializers.ModelSerializer):
    schedule_type = ScheduleTypeListSerializer(many=False, source='get_schedule_type')
    activity_type = ActivityTypeListSerializer(many=False, source='get_activity_type')
    bill_cycle = BillCycleListSerializer(many=False, source='get_bill_cycle')
    schedule_status = ScheduleStatusListSerializer(many=False, source='get_schedule_status')

    class Meta:
        model = Schedule
        fields = ('id_string',)


class ScheduleSerializer(serializers.ModelSerializer):
    schedule_type_id   = serializers.CharField(required=False, max_length=200, error_messages={"required":""})
    activity_type_id   = serializers.CharField(required=False, max_length=200, error_messages={"required":""})
    bill_cycle_id      = serializers.CharField(required=False, max_length=200, error_messages={"required":""})
    schedule_status_id = serializers.CharField(required=False, max_length=200, error_messages={"required":""})

    class Meta:
        model = Schedule
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_schedule_validated_data(validated_data)
        with transaction.atomic():
            schedule_obj = super(ScheduleSerializer, self).create(validated_data)
            schedule_obj.created_by = user.id
            schedule_obj.created_date = datetime.utcnow()
            schedule_obj.tenant = user.tenant
            schedule_obj.utility = user.utility
            schedule_obj.save()
            return schedule_obj

    def update(self, instance, validated_data, user):
        validated_data = set_schedule_validated_data(validated_data)
        with transaction.atomic():
            schedule_obj = super(ScheduleSerializer, self).update(instance, validated_data)
            schedule_obj.updated_by = user.id
            schedule_obj.updated_date = datetime.utcnow()
            schedule_obj.save()
            return schedule_obj