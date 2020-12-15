__author__ = "priyanka"

from rest_framework import serializers
from v1.commonapp.models.frequency import Frequency as FrequecyTbl
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.campaign.serializers.campaign_type import CampaignTypeListSerializer
from v1.commonapp.serializers.channel import ChannelListSerializer
from v1.commonapp.common_functions import set_frequency_validated_data
from django.db import transaction
from datetime import datetime


class FrequencySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    campaign_type_id = serializers.CharField(required=True, max_length=200)
    channel_type_id =  serializers.CharField(required=True, max_length=200)

    class Meta:
        model = FrequecyTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_frequency_validated_data(validated_data)
            frequency_obj = super(FrequencySerializer, self).create(validated_data)
            frequency_obj.created_by = user.id
            frequency_obj.updated_by = user.id
            frequency_obj.save()
            return frequency_obj

    def update(self, instance, validated_data, user):
        validated_data = set_frequency_validated_data(validated_data)
        with transaction.atomic():
            frequency_obj = super(FrequencySerializer, self).update(instance, validated_data)
            frequency_obj.updated_by = user.id
            frequency_obj.updated_date = datetime.utcnow()
            frequency_obj.save()
            return frequency_obj

class FrequencyViewSerializer(serializers.ModelSerializer):
    
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = FrequecyTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')

class FrequencyListSerializer(serializers.ModelSerializer):
    campaign = CampaignTypeListSerializer(many="False", source="get_campaign")
    channel = ChannelListSerializer(many="False",source="get_channel")

    class Meta:
        model = FrequecyTbl
        fields = ('name', 'id_string','campaign','channel','created_date','is_active','created_by')