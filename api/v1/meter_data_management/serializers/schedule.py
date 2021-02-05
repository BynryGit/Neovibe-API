__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from api.messages import DATA_ALREADY_EXISTS
from rest_framework import serializers, status
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.commonapp.views.settings_reader import SettingReader
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_data_management.models.schedule import Schedule as ScheduleTbl
from v1.meter_data_management.models.schedule_log import ScheduleLog as ScheduleLogTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.views.common_function import set_schedule_validated_data
setting_reader = SettingReader()


class ScheduleShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleTbl
        fields = ('id_string','name')


class ScheduleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    activity_type_id = GlobalLookupShortViewSerializer(many=False, source='get_activity_type')
    frequency_id = GlobalLookupShortViewSerializer(many=False, source='get_frequency_name')
    repeat_every_id = GlobalLookupShortViewSerializer(many=False, source='get_repeat_every_name')
    recurring_id = GlobalLookupShortViewSerializer(many=False, source='get_recurring_name')
    start_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    end_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    schedule_status = ChoiceField(choices=ScheduleTbl.SCHEDULE_STATUS)

    class Meta:
        model = ScheduleTbl
        fields = ('id_string', 'name', 'description', 'schedule_status', 'start_date', 'end_date', 'created_date',
                  'updated_date', 'created_by', 'updated_by', 'recurring_id', 'repeat_every_id', 'read_cycle_id',
                  'activity_type_id', 'frequency_id', 'occurs_on', 'tenant', 'utility')


class ScheduleSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=True)
    read_cycle_id = serializers.UUIDField(required=True)
    activity_type_id = serializers.UUIDField(required=True)
    frequency_id = serializers.UUIDField(required=False)
    repeat_every_id = serializers.UUIDField(required=False)
    recurring_id = serializers.UUIDField(required=False)
    occurs_on = serializers.JSONField(required=False)

    class Meta:
        model = ScheduleTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_schedule_validated_data(validated_data)
        if ScheduleTbl.objects.filter(tenant=user.tenant, utility_id=validated_data['utility_id'],
                                      read_cycle_id=validated_data["read_cycle_id"], is_active=True).exists():
            raise CustomAPIException(DATA_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                schedule_obj = super(ScheduleSerializer, self).create(validated_data)
                schedule_obj.tenant = user.tenant
                schedule_obj.created_by = user.id
                schedule_obj.save()
                reccuring_obj = get_global_lookup_by_id(schedule_obj.recurring_id)
                if reccuring_obj.key == 'no':
                    ScheduleLogTbl(
                        tenant=schedule_obj.tenant,
                        utility=schedule_obj.utility,
                        schedule_id=schedule_obj.id,
                        read_cycle_id=schedule_obj.read_cycle_id,
                        activity_type_id=schedule_obj.activity_type_id,
                        date_and_time=timezone.now(),
                        recurring_id=schedule_obj.recurring_id,
                    ).save()
                return schedule_obj

    def update(self, instance, validated_data, user):
        validated_data = set_schedule_validated_data(validated_data)
        with transaction.atomic():
            schedule_obj = super(ScheduleSerializer, self).update(instance, validated_data)
            schedule_obj.tenant = user.tenant
            schedule_obj.updated_by = user.id
            schedule_obj.updated_date = timezone.now()
            schedule_obj.save()
            reccuring_obj = get_global_lookup_by_id(schedule_obj.recurring_id)
            if reccuring_obj.key == 'no':
                ScheduleLogTbl.objects.filter(schedule_id=schedule_obj.id, is_active=True).update(is_active=False)
                ScheduleLogTbl(
                    tenant=schedule_obj.tenant,
                    utility=schedule_obj.utility,
                    schedule_id=schedule_obj.id,
                    read_cycle_id=schedule_obj.read_cycle_id,
                    activity_type_id=schedule_obj.activity_type_id,
                    date_and_time=timezone.now(),
                    recurring_id=schedule_obj.recurring_id,
                ).save()
            else:
                ScheduleLogTbl.objects.filter(schedule_id=schedule_obj.id, is_active=True).update(is_active=False)
            return schedule_obj
