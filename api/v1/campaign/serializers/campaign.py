__author__ = "Priyanka"

from rest_framework import serializers
from v1.campaign.models.campaign import Campaign as CampaignTbl
from v1.campaign.models.campaign_status import CampaignStatus
from v1.campaign.models.campaign_objective import CampaignObjective
from v1.campaign.models.campaign_group import CampaignGroup


class CampaignGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignGroup
        fields = ('name','id_string')

class CampaignObjectiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignObjective
        fields = ('name','id_string')

class CampaignStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignStatus
        fields = ('name','id_string')


class CampaignListSerializer(serializers.ModelSerializer):
    group = CampaignGroupSerializer(many=False, required=True, source='get_group')
    objective = CampaignObjectiveSerializer(many=False, required=True, source='get_objective')
    status = CampaignStatusSerializer(many=False, required=True, source='get_status')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = CampaignTbl
        fields = ('id_string', 'tenant_name', 'name',  'description',
                  'frequency_id','potential_consumers','actual_consumers','budget_amount','actual_amount','category_id',
                  'sub_category_id','start_date','end_date','area_id','sub_area_id','objective','group','status',
                  'is_active')

# class CampaignSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CampaignTbl
#         fields = ('name', 'id_string')

class CampaignViewSerializer(serializers.ModelSerializer):
    group = CampaignGroupSerializer(many=False, required=True, source='get_group')
    objective = CampaignObjectiveSerializer(many=False, required=True, source='get_objective')
    status = CampaignStatusSerializer(many=False, required=True, source='get_status')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = CampaignTbl
        fields = ('id_string', 'tenant_name', 'name',  'description',
                  'frequency_id','potential_consumers','actual_consumers','budget_amount','actual_amount','category_id',
                  'sub_category_id','start_date','end_date','area_id','sub_area_id','objective','group','status',
                  'is_active')


class CampaignSerializer(serializers.ModelSerializer):
    tenant_id_string = serializers.UUIDField(required=True)
    utility_id_string = serializers.UUIDField(required=True)

    class Meta:
        model = CampaignTbl
        fields = ('id_string', 'tenant_name', 'name',  'description',
                  'frequency_id','potential_consumers','actual_consumers','budget_amount','actual_amount','category_id',
                  'sub_category_id','start_date','end_date','area_id','sub_area_id','objective','group','status',
                  'is_active')

    def create(self, validated_data, user):
        with transaction.atomic():
            advertisements = []
            if 'advertisement' in validated_data:
                advertisements = validated_data.pop('advertisement')

            campaign_obj = super(CampaignSerializer, self).create(validated_data)
            campaign_obj.created_by = user
            campaign_obj.created_date = datetime.now()
            campaign_obj.save()
            for advertisement in advertisements:
                advertisement['campaign_id'] = campaign_obj.id
                advertisement_obj = AdvertisementSerializer(**advertisement)
            return campaign_obj, advertisement_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            campaign_obj = super(CampaignSerializer, self).update(instance, validated_data)
            campaign_obj.updated_by = user
            campaign_obj.updated_date = datetime.now()
            campaign_obj.save()
            return campaign_obj