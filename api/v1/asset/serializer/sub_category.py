__author__ = "Priyanka"

from rest_framework import serializers
from v1.asset.models.asset_sub_category import AssetSubCategory
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT

class AssetSubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetSubCategory
        fields = ('name','id_string')

class AssetSubCategoryViewSerializer(serializers.ModelSerializer):
    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = AssetSubCategory
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')