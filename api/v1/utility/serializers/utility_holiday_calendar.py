from rest_framework import serializers, status
from django.db import transaction
from v1.utility.views.common_functions import set_holiday_validated_data
from datetime import datetime
from api.messages import HOLIDAY_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_holiday_calendar import UtilityHolidayCalendar as UtilityHolidayCalendarTbl
from v1.utility.serializers.utility_leave_type import UtilityLeaveTypeListSerializer


class HolidayViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityHolidayCalendarTbl
        fields = ('name', 'id_string',  'start_time','end_time', 'date', 'description', 'utility', 'utility_id_string', 'tenant', 'tenant_id_string')


class HolidaySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    description = serializers.CharField(required=True, max_length=200)
    holiday_type_id = serializers.CharField(required=False, max_length=200)
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityHolidayCalendarTbl
        fields = ('name', 'id_string',  'start_time', 'end_time', 'date', 'description', 'holiday_type_id', 'utility_id', 'tenant_id')

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_holiday_validated_data(validated_data)
            if UtilityHolidayCalendarTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                        utility_id=validated_data['utility_id'],date=validated_data['date']).exists():
                raise CustomAPIException(HOLIDAY_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                holiday_obj = super(HolidaySerializer, self).create(validated_data)
                holiday_obj.created_by = user.id
                holiday_obj.updated_by = user.id
                holiday_obj.save()
                return holiday_obj

    def update(self, instance, validated_data, user):
        validated_data = set_holiday_validated_data(validated_data)
        if UtilityHolidayCalendarTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                        utility_id=validated_data['utility_id'],date=validated_data['date']).exists():
                raise CustomAPIException(HOLIDAY_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                holiday_obj = super(HolidaySerializer, self).update(instance, validated_data)
                holiday_obj.tenant = user.tenant
                holiday_obj.updated_by = user.id
                holiday_obj.updated_date = datetime.utcnow()
                holiday_obj.save()
                return holiday_obj


class HolidayListSerializer(serializers.ModelSerializer):
    holiday_type = UtilityLeaveTypeListSerializer(source="get_holiday_type")

    class Meta:
        model = UtilityHolidayCalendarTbl
        fields = ('name', 'id_string', 'start_time', 'end_time', 'date', 'description', 'holiday_type', 'created_date', 'is_active', 'created_by')