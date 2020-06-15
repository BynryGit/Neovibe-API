__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_reading.models.schedule import Schedule as ScheduleTbl
from v1.meter_reading.serializers.activity_type import ActivityTypeShortViewSerializer
from v1.meter_reading.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.meter_reading.serializers.schedule_status import ScheduleStatusShortViewSerializer
from v1.meter_reading.serializers.schedule_type import ScheduleTypeShortViewSerializer
from v1.meter_reading.views.common_functions import set_schedule_validated_data


class ScheduleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    schedule_type_id = ScheduleTypeShortViewSerializer(many=False, source='get_schedule_type')
    activity_type_id = ActivityTypeShortViewSerializer(many=False, source='get_activity_type')
    bill_cycle_id = BillCycleShortViewSerializer(many=False, source='get_bill_cycle')
    schedule_status_id = ScheduleStatusShortViewSerializer(many=False, source='get_schedule_status')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ScheduleTbl
        fields = ('id_string','bill_month', 'start_date', 'end_date', 'due_date', 'is_valid_next_cycle', 'is_imported',
                  'is_uploaded', 'schedule_type_id', 'activity_type_id', 'bill_cycle_id', 'schedule_status_id',
                  'created_date', 'updated_date', 'tenant', 'utility')


class ScheduleSerializer(serializers.ModelSerializer):
    schedule_type_id = serializers.UUIDField(required=True)
    activity_type_id = serializers.UUIDField(required=True)
    bill_cycle_id = serializers.UUIDField(required=True)
    schedule_status_id = serializers.UUIDField(required=True)

    class Meta:
        model = ScheduleTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_schedule_validated_data(validated_data)
        if ScheduleTbl.objects.filter(tenant=user.tenant, utility_id=1,
                                      bill_cycle_id=validated_data["bill_cycle_id"]).exists():
            return False
        with transaction.atomic():
            supplier_obj = super(ScheduleSerializer, self).create(validated_data)
            supplier_obj.tenant = user.tenant
            supplier_obj.utility_id = 1
            supplier_obj.created_by = user.id
            supplier_obj.save()
            return supplier_obj

    def update(self, instance, validated_data, user):
        validated_data = set_schedule_validated_data(validated_data)
        with transaction.atomic():
            supplier_obj = super(ScheduleSerializer, self).update(instance, validated_data)
            supplier_obj.tenant = user.tenant
            supplier_obj.utility_id = 1
            supplier_obj.updated_by = user.id
            supplier_obj.updated_date = timezone.now()
            supplier_obj.save()
            return supplier_obj
