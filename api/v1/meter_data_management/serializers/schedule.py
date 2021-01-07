__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from api.messages import DATA_ALREADY_EXISTS
from rest_framework import serializers, status
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.area import AreaShortViewSerializer
from v1.commonapp.serializers.city import CityShortViewSerializer
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.premises import PremisesShortViewSerializer
from v1.commonapp.serializers.sub_area import SubAreaShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.commonapp.serializers.zone import ZoneShortViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_data_management.models.schedule import Schedule as ScheduleTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.views.common_functions import set_schedule_validated_data


class ScheduleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    city_id = CityShortViewSerializer(many=False, source='get_city_name')
    zone_id = ZoneShortViewSerializer(many=False, source='get_zone_name')
    # division_id = DivisionShortViewSerializer(many=False, source='get_division_name')
    area_id = AreaShortViewSerializer(many=False, source='get_area_name')
    sub_area_id = SubAreaShortViewSerializer(many=False, source='get_sub_area_name')
    # premises_id = PremisesShortViewSerializer(many=False, source='get_premises_name')
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    consumer_type_id = GlobalLookupShortViewSerializer(many=False, source='get_consumer_type_name')
    schedule_type_id = GlobalLookupShortViewSerializer(many=False, source='get_schedule_type_id_name')
    activity_type_id = GlobalLookupShortViewSerializer(many=False, source='get_activity_type_id_name')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    start_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    end_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    due_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ScheduleTbl
        fields = ('id_string','month', 'start_date', 'end_date', 'due_date', 'created_date', 'updated_date',
                  'schedule_status', 'created_by', 'updated_by', 'city_id',
                  'zone_id', 'division_id', 'area_id', 'sub_area_id', 'premises_id', 'read_cycle_id',
                  'consumer_type_id', 'schedule_type_id', 'activity_type_id', 'tenant', 'utility')


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
            raise CustomAPIException(DATA_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
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
