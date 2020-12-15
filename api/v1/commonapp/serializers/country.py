__author__ = "aki"

from rest_framework import serializers, status
from v1.commonapp.models.country import Country as CountryTbl
from api.messages import *
from django.db import transaction
from v1.commonapp.serializers.region import RegionSerializer, RegionListSerializer
from v1.utility.serializers.utility_region import UtilityRegionListSerializer
from v1.commonapp.models.region import get_region_by_id
from v1.commonapp.common_functions import set_country_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from datetime import datetime
from api.messages import COUNTRY_ALREADY_EXIST


class CountryViewSerializer(serializers.ModelSerializer):
    
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = CountryTbl
        fields = ('name', 'id_string','utility', 'utility_id_string','tenant', 'tenant_id_string')


class CountrySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    region_id = serializers.CharField(required=False, max_length=200)
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = CountryTbl
        fields = ('name', 'id_string', 'region_id', 'utility_id', 'tenant_id')

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_country_validated_data(validated_data)
            if CountryTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                         utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(COUNTRY_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                country_obj = super(CountrySerializer, self).create(validated_data)
                country_obj.created_by = user.id
                country_obj.updated_by = user.id
                country_obj.save()
                return country_obj

    def update(self, instance, validated_data, user):
        validated_data = set_country_validated_data(validated_data)
        with transaction.atomic():
            country_obj = super(CountrySerializer, self).update(instance, validated_data)
            country_obj.tenant = user.tenant
            country_obj.updated_by = user.id
            country_obj.updated_date = datetime.utcnow()
            country_obj.save()
            return country_obj


class CountryListSerializer(serializers.ModelSerializer):
    region = UtilityRegionListSerializer(source="get_utility_region")
    

    class Meta:
        model = CountryTbl
        fields = ('name', 'id_string', 'region','created_date','is_active','created_by')
