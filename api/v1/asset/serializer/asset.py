__author__ = "Priyanka"

from rest_framework import serializers
from datetime import datetime
from django.db import transaction
from v1.asset.models.asset_master import Asset as AssetTbl
from v1.asset.models.asset_status import AssetStatus as AssetStatusTbl
from v1.asset.views.common_function import set_asset_validated_data

class AssetStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetStatusTbl
        fields = ('id_string','name')

class AssetListSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    status_id = AssetStatusSerializer(many=False, required=True, source='get_status')
    class Meta:
        model = AssetTbl
        fields = ('__all__')

class AssetViewSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    status_id = AssetStatusSerializer(many=False, required=True, source='get_status')
    class Meta:
        model = AssetTbl
        fields = ('id_string', 'asset_no', 'description','serial_no','manufacturer','make','model','city_id',
                   'area_id', 'sub_area_id','address','category_id','sub_category_id','lat','long','manufacturing_date',
                   'installation_date','expiry_date','asset_life','asset_value','deprecation_method','deprecation_rate',
                   'status_id','flag')


class AssetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=200)
    asset_no = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, max_length=200)
    serial_no = serializers.CharField(required=False, max_length=200)
    manufacturer = serializers.CharField(required=False, max_length=200)
    make = serializers.CharField(required=False, max_length=200)
    model = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    subarea_id = serializers.CharField(required=False, max_length=200)
    address = serializers.CharField(required=False, max_length=200)
    category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    lat = serializers.CharField(required=False, max_length=200)
    long = serializers.CharField(required=False, max_length=200)
    manufacturing_date = serializers.CharField(required=False, max_length=200)
    installation_date = serializers.CharField(required=False, max_length=200)
    expiry_date = serializers.CharField(required=False, max_length=200)
    asset_life = serializers.CharField(required=False, max_length=200)
    asset_value = serializers.CharField(required=False, max_length=200)
    deprecation_method = serializers.CharField(required=False, max_length=200)
    deprecation_rate = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    flag = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = AssetTbl
        fields =  ('id_string', 'asset_no', 'description','serial_no','manufacturer','make','model','city_id',
                   'area_id', 'sub_area_id','address','category_id','sub_category_id','lat','long','manufacturing_date',
                   'installation_date','expiry_date','asset_life','asset_value','deprecation_method','deprecation_rate',
                   'status_id','flag')


    def create(self, validated_data, user):
        validated_data = set_asset_validated_data(validated_data)
        if AssetTbl.objects.filter(**validated_data).exists():
            return False
        else:
            with transaction.atomic():
                asset_obj = super(AssetSerializer, self).create(validated_data)
                asset_obj.created_by = user.id
                asset_obj.created_date = datetime.now()
                asset_obj.tenant = user.tenant
                asset_obj.utility = user.utility
                asset_obj.save()
                return asset_obj

    def update(self, instance, validated_data, user):
            validated_data = set_asset_validated_data(validated_data)
            with transaction.atomic():
                asset_obj = super(AssetSerializer, self).update(instance, validated_data)
                asset_obj.updated_by = user.id
                asset_obj.updated_date = datetime.now()
                asset_obj.save()
                return asset_obj