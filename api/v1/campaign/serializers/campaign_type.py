from rest_framework import serializers, status
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from v1.campaign.models.campaign_type import CampaignType as CampaignTypeTbl
from django.db import transaction
from datetime import datetime
from api.messages import CAMPAIGN_TYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.campaign.views.common_functions import set_campaign_type_validated_data

class CampaignTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = CampaignTypeTbl
        fields = '__all__'


class CampaignTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field Campaign Type name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = CampaignTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_campaign_type_validated_data(validated_data)
            if CampaignTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                        utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(CAMPAIGN_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                
                campaign_obj = super(CampaignTypeSerializer, self).create(validated_data)
                campaign_obj.created_by = user.id
                campaign_obj.updated_by = user.id
                campaign_obj.save()
                return campaign_obj

    def update(self, instance, validated_data, user):
        validated_data = set_campaign_type_validated_data(validated_data)
        with transaction.atomic():
            campaign_obj = super(CampaignTypeSerializer, self).update(instance, validated_data)
            campaign_obj.tenant = user.tenant
            campaign_obj.updated_by = user.id
            campaign_obj.updated_date = datetime.utcnow()
            campaign_obj.save()
            return campaign_obj


class CampaignTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTypeTbl
        fields = ('name', 'id_string','is_active','created_by','created_date')