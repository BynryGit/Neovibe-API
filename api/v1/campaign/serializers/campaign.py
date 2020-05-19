__author__ = "Priyanka"

from rest_framework import serializers
from v1.campaign.models.campaign import Campaign as CampaignTbl
from v1.campaign.models.campaign_status import CampaignStatus
from v1.campaign.models.campaign_objective import CampaignObjective
from v1.campaign.models.campaign_group import CampaignGroup
from v1.campaign.views.common_functions import set_validated_data
from datetime import datetime
from django.db import transaction

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
    name = serializers.CharField(required=False, max_length=200)
    group_id = serializers.CharField(required=False, max_length=200)
    objective_id = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, max_length=200)
    frequency_id = serializers.CharField(required=False, max_length=200)
    potential_consumers = serializers.CharField(required=False, max_length=200)
    actual_consumers = serializers.CharField(required=False, max_length=200)
    budget_amount = serializers.CharField(required=False, max_length=200)
    actual_amount = serializers.CharField(required=False, max_length=200)
    category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    start_date = serializers.CharField(required=False, max_length=200)
    end_date = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = CampaignTbl
        fields =  ('id_string', 'name', 'group_id','objective_id', 'description',
                  'frequency_id','potential_consumers','actual_consumers','budget_amount','actual_amount','category_id',
                  'sub_category_id','start_date','end_date','area_id','sub_area_id','status_id')

    def create(self, validated_data, user):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            campaign_obj = super(CampaignSerializer, self).create(validated_data)
            campaign_obj.created_by = user.id
            campaign_obj.created_date = datetime.now()
            campaign_obj.tenant = user.tenant
            campaign_obj.utility = user.utility
            campaign_obj.save()
            return campaign_obj

    def update(self, instance, validated_data, user):
            validated_data = set_validated_data(validated_data)
            with transaction.atomic():
                campaign_obj = super(CampaignSerializer, self).update(instance, validated_data)
                campaign_obj.updated_by = user.id
                campaign_obj.updated_date = datetime.now()
                campaign_obj.save()
                return campaign_obj