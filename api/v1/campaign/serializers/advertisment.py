__author__ = "Priyanka"

from rest_framework import serializers

from v1.campaign.serializers.campaign import CampaignGroupSerializer,CampaignObjectiveSerializer
from v1.campaign.models.campaign import Campaign as CampaignTbl
from v1.campaign.models.advertisement import Advertisements
from v1.campaign.models.advertisement_type import AdvertisementType
from v1.campaign.models.advert_status import AdvertStatus

class AdvertisementTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvertisementType
        fields = ('name','id_string')

class AdvertStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvertStatus
        fields = ('name','id_string')

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTbl
        fields = ('name', 'id_string')

class AdvertismentViewSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer(many=False, required=True, source='get_campaign')
    group = CampaignGroupSerializer(many=False, required=True, source='get_group')
    objective = CampaignObjectiveSerializer(many=False, required=True, source='get_objective')
    advert_type = AdvertisementTypeSerializer(many=False, required=True, source='get_advert_type')
    status = AdvertStatusSerializer(many=False, required=True, source='get_advert_status')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = Advertisements
        fields = ('id_string', 'tenant_name', 'name', 'description',
                  'potential_consumers', 'actual_consumers', 'budget_amount', 'actual_amount',
                   'start_date', 'end_date','campaign','advert_type','objective', 'group', 'status',
                  'is_active')

class AdvertismentListSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer(source='get_campaign')
    group = CampaignGroupSerializer(many=False, required=True, source='get_group')
    objective = CampaignObjectiveSerializer(many=False, required=True, source='get_objective')
    advert_type = AdvertisementTypeSerializer(many=False, required=True, source='get_advert_type')
    status = AdvertStatusSerializer(many=False, required=True, source='get_advert_status')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = Advertisements
        fields = ('id_string', 'tenant_name', 'name', 'description',
                  'potential_consumers', 'actual_consumers', 'budget_amount', 'actual_amount',
                  'start_date', 'end_date', 'campaign', 'advert_type', 'objective', 'group', 'status',
                  'is_active')