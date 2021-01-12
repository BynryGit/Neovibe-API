<<<<<<< HEAD
from rest_framework import serializers, status
from django.db import transaction
from v1.meter_data_management.views.common_function import set_read_cycle_validated_data
from datetime import datetime
from api.messages import HOLIDAY_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_data_management.models.read_cycle import ReadCycle as ReadCycleTbl
from v1.commonapp.serializers.city import CityListSerializer
from v1.commonapp.serializers.zone import ZoneListSerializer
from v1.commonapp.serializers.division import DivisionListSerializer
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.serializers.sub_area import SubAreaListSerializer


class ReadCycleViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ReadCycleTbl
        fields = ('name', 'id_string', 'utility', 'utility_id_string', 'tenant', 'tenant_id_string')


class ReadCycleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    description = serializers.CharField(required=True, max_length=200)
    holiday_type_id = serializers.CharField(required=False, max_length=200)
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ReadCycleTbl
        fields = ('name', 'id_string')

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_read_cycle_validated_data(validated_data)
            if ReadCycleTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                           utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(HOLIDAY_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                read_cycle_obj = super(ReadCycleSerializer, self).create(validated_data)
                read_cycle_obj.created_by = user.id
                read_cycle_obj.updated_by = user.id
                read_cycle_obj.save()
                return read_cycle_obj

    def update(self, instance, validated_data, user):
        validated_data = set_read_cycle_validated_data(validated_data)
        with transaction.atomic():
            read_cycle_obj = super(ReadCycleSerializer, self).update(instance, validated_data)
            read_cycle_obj.tenant = user.tenant
            read_cycle_obj.updated_by = user.id
            read_cycle_obj.updated_date = datetime.utcnow()
            read_cycle_obj.save()
            return read_cycle_obj


class ReadCycleListSerializer(serializers.ModelSerializer):
    city = CityListSerializer(source="get_city")
    zone = ZoneListSerializer(source="get_zone")
    division = DivisionListSerializer(source="get_division")
    area = AreaListSerializer(source="get_area")
    subarea = SubAreaListSerializer(source="get_subarea")

    class Meta:
        model = ReadCycleTbl
        fields = ('name', 'id_string', 'city', 'zone', 'division','area', 'subarea', 'created_date', 'is_active', 'created_by')
=======
__author__ = "aki"

from rest_framework import serializers, status
from v1.meter_data_management.models.read_cycle import ReadCycle as ReadCycleTbl


class ReadCycleShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadCycleTbl
        fields = ('id_string','label')
>>>>>>> 4540cf6d2cde97aad5f56375dea574d1906a2737
