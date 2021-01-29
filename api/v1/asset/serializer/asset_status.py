__author__ = "Priyanka"

from rest_framework import serializers
from v1.asset.models.asset_status import AssetStatus as AssetStatusTbl
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()

class AssetStatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetStatusTbl
        fields = ('name','id_string')

class AssetStatusViewSerializer(serializers.ModelSerializer):
    def get_created_date(self, obj):
        return obj.created_date.strftime(setting_reader.get_display_date_format())

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = AssetStatusTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')