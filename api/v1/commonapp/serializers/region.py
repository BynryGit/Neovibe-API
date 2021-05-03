__author__ = "chinmay"

from rest_framework import serializers, status
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from v1.commonapp.models.region import Region as RegionTbl
from django.db import transaction
from v1.commonapp.common_functions import set_region_validated_data
from datetime import datetime
from api.messages import REGION_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_region import UtilityRegion as UtilityRegionTbl


class TenantRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantRegionTbl
        fields = ('id_string', 'region')


class RegionViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityRegionTbl
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    region_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityRegionTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_region_validated_data(validated_data)
            if UtilityRegionTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                               utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(REGION_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:

                region_obj = super(RegionSerializer, self).create(validated_data)
                region_obj.created_by = user.id
                region_obj.save()
                return region_obj

    def update(self, instance, validated_data, user):
        validated_data = set_region_validated_data(validated_data)
        if UtilityRegionTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                           utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(REGION_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                region_obj = super(RegionSerializer, self).update(instance, validated_data)
                region_obj.tenant = user.tenant
                region_obj.updated_by = user.id
                region_obj.updated_date = datetime.utcnow()
                region_obj.save()
                return region_obj


class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionTbl
        fields = ('name', 'id_string', 'is_active', 'created_by', 'created_date')
