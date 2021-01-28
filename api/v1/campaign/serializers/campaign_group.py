
from rest_framework import serializers
from v1.campaign.models.campaign_group import CampaignGroup
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()

class CampaignGroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignGroup
        fields = ('name', 'id_string')

class CampaignGroupViewSerializer(serializers.ModelSerializer):

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = CampaignGroup
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')