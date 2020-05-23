from rest_framework import serializers
from v1.campaign.models.campaign_status import CampaignStatus
from api.settings import DISPLAY_DATE_TIME_FORMAT

class CampaignStatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignStatus
        fields = ('name','id_string')

class CampaignStatusViewSerializer(serializers.ModelSerializer):
    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = CampaignStatus
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')