
from rest_framework import serializers
from v1.campaign.models.campaign_group import CampaignGroup

class CampaignGroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignGroup
        fields = ('name', 'id_string')

class CampaignGroupViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = CampaignGroup
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')