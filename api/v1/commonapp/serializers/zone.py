from v1.commonapp.models.zone import Zone as ZoneTbl
from rest_framework import serializers, status
from v1.commonapp.serializers.city import CityListSerializer, CityViewSerializer
from api.messages import *
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_zone_validated_data
from api.messages import ZONE_ALREADY_EXIST


class ZoneShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneTbl
        fields = ('id_string', 'name')


class ZoneViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = ZoneTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class ZoneSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ZoneTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_zone_validated_data(validated_data)
            if ZoneTbl.objects.filter(name=validated_data['name'], tenant=user.tenant,
                                      utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(ZONE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
            else:
                zone_obj = super(ZoneSerializer, self).create(validated_data)
                zone_obj.created_by = user.id
                zone_obj.save()
                return zone_obj

    def update(self, instance, validated_data, user):
        validated_data = set_zone_validated_data(validated_data)
        if ZoneTbl.objects.filter(name=validated_data['name'], tenant=user.tenant,
                                  utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(ZONE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                zone_obj = super(ZoneSerializer, self).update(instance, validated_data)
                zone_obj.updated_by = user.id
                zone_obj.updated_date = datetime.utcnow()
                zone_obj.save()
                return zone_obj


class ZoneListSerializer(serializers.ModelSerializer):
    city = CityListSerializer(source="get_city")

    class Meta:
        model = ZoneTbl
        fields = ('name', 'id_string', 'city','is_active','created_by','created_date')
