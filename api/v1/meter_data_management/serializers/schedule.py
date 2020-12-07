__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.serializers.sub_area import SubAreaListSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.schedule import Schedule as ScheduleTbl
from v1.meter_data_management.serializers.activity_type import ActivityTypeShortViewSerializer
from v1.meter_data_management.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.meter_data_management.serializers.schedule_status import ScheduleStatusShortViewSerializer
from v1.meter_data_management.serializers.schedule_type import ScheduleTypeShortViewSerializer
from v1.meter_data_management.views.common_functions import set_schedule_validated_data


class ScheduleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    schedule_type_id = ScheduleTypeShortViewSerializer(many=False, source='get_schedule_type')
    activity_type_id = ActivityTypeShortViewSerializer(many=False, source='get_activity_type')
    area_id = AreaListSerializer(many=False, source='get_area_name')
    sub_area_id = SubAreaListSerializer(many=False, source='get_sub_area_name')
    bill_cycle_id = BillCycleShortViewSerializer(many=False, source='get_bill_cycle')
    schedule_status_id = ScheduleStatusShortViewSerializer(many=False, source='get_schedule_status')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    start_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    end_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    due_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ScheduleTbl
        fields = ('id_string','bill_month', 'start_date', 'end_date', 'due_date', 'is_valid_next_cycle', 'is_imported',
                  'is_uploaded', 'created_date', 'updated_date', 'schedule_type_id', 'activity_type_id', 'area_id',
                  'sub_area_id', 'bill_cycle_id', 'schedule_status_id', 'tenant', 'utility')


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
            schedule_obj = super(ScheduleSerializer, self).create(validated_data)
            schedule_obj.tenant = user.tenant
            schedule_obj.utility_id = 1
            schedule_obj.created_by = user.id
            schedule_obj.save()
            return schedule_obj

    def update(self, instance, validated_data, user):
        validated_data = set_schedule_validated_data(validated_data)
        with transaction.atomic():
            schedule_obj = super(ScheduleSerializer, self).update(instance, validated_data)
            schedule_obj.tenant = user.tenant
            schedule_obj.utility_id = 1
            schedule_obj.updated_by = user.id
            schedule_obj.updated_date = timezone.now()
            schedule_obj.save()
            return schedule_obj
