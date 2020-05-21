__author__ = "Priyanka"

from rest_framework import serializers
from v1.asset.models.asset_category import AssetCategory

class AssetCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = ('name','id_string')

class AssetCategoryViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = AssetCategory
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')