__author__ = "Priyanka"

from rest_framework import serializers
from datetime import datetime
from django.db import transaction
from v1.campaign.serializers.campaign import CampaignGroupSerializer,CampaignObjectiveSerializer
from v1.campaign.models.campaign import Campaign as CampaignTbl
from v1.campaign.models.advertisement import Advertisements
from v1.campaign.models.advertisement_type import AdvertisementType
from v1.campaign.models.advert_status import AdvertStatus
from v1.campaign.views.common_functions import set_validated_data
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()

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

    def get_created_date(self, obj):
        return obj.created_date.strftime(setting_reader.get_display_date_format())

    def get_start_date(self, obj):
        return obj.start_date.strftime(setting_reader.get_display_date_format())

    def get_end_date(self, obj):
        return obj.end_date.strftime(setting_reader.get_display_date_format())

    campaign_id = CampaignSerializer(many=False, required=True, source='get_campaign')
    group_id = CampaignGroupSerializer(many=False, required=True, source='get_group')
    objective_id = CampaignObjectiveSerializer(many=False, required=True, source='get_objective')
    type_id = AdvertisementTypeSerializer(many=False, required=True, source='get_advert_type')
    status_id = AdvertStatusSerializer(many=False, required=True, source='get_advert_status')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    created_date = serializers.SerializerMethodField('get_created_date')
    start_date = serializers.SerializerMethodField('get_start_date')
    end_date = serializers.SerializerMethodField('get_end_date')

    class Meta:
        model = Advertisements
        fields = ('id_string', 'tenant_name', 'name', 'description',
                  'potential_consumers', 'actual_consumers', 'budget_amount', 'actual_amount',
                  'start_date', 'end_date', 'campaign_id', 'type_id','objective_id', 'group_id',
                  'status_id','is_active','created_date')

class AdvertismentListSerializer(serializers.ModelSerializer):

    campaign = CampaignSerializer(many=False, required=True,source='get_campaign')
    group = CampaignGroupSerializer(many=False, required=True, source='get_group')
    objective = CampaignObjectiveSerializer(many=False, required=True, source='get_objective')
    advert_type = AdvertisementTypeSerializer(many=False, required=True, source='get_advert_type')
    status = AdvertStatusSerializer(many=False, required=True, source='get_advert_status')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    start_date = serializers.DateTimeField(format=setting_reader.get_display_date_format())
    end_date = serializers.DateTimeField(format=setting_reader.get_display_date_format())

    class Meta:
        model = Advertisements
        fields = ('id_string', 'tenant_name', 'name', 'description',
                  'potential_consumers', 'actual_consumers', 'budget_amount', 'actual_amount',
                  'start_date', 'end_date', 'campaign', 'advert_type', 'objective', 'group', 'status',
                  'is_active','created_date')

class AdvertisementSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    name = serializers.CharField(required=False, max_length=200)
    potential_consumers = serializers.CharField(required=False, max_length=200)
    actual_consumers = serializers.CharField(required=False, max_length=200)
    budget_amount = serializers.CharField(required=False, max_length=200)
    actual_amount = serializers.CharField(required=False, max_length=200)
    start_date = serializers.DateTimeField(format="%Y-%m-%d")
    end_date = serializers.DateTimeField(format="%Y-%m-%d")
    campaign_id = serializers.CharField(required=False, max_length=200)
    group_id = serializers.CharField(required=False, max_length=200)
    objective_id = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, max_length=200)
    frequency_id = serializers.CharField(required=False, max_length=200)
    type_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    class Meta:
        model = Advertisements
        fields = ('__all__')

    def create(self,validated_data,user,campaign_obj):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            advert_obj = super(AdvertisementSerializer, self).create(validated_data)
            advert_obj.campaign_id = campaign_obj.id
            advert_obj.is_active = True
            advert_obj.created_by = user.id
            advert_obj.created_date = datetime.now()
            advert_obj.tenant = user.tenant
            advert_obj.utility = user.utility
            advert_obj.save()
            return advert_obj

    def update(self, instance, validated_data, user):
            validated_data = set_validated_data(validated_data)
            advert_obj = super(AdvertisementSerializer, self).update(instance, validated_data)
            advert_obj.updated_by = user.id
            advert_obj.updated_date = datetime.now()
            advert_obj.save()
            return advert_obj