from rest_framework import serializers, status
from v1.campaign.models.advertisement_subtype import AdvertisementSubType as AdvertisementSubTypeTbl
from api.settings import DISPLAY_DATE_TIME_FORMAT
from django.db import transaction
from datetime import datetime
from api.messages import ADVERTISEMENT_SUBTYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.campaign.views.common_functions import set_advertisement_subtype_validated_data
from v1.campaign.serializers.advertisement_type import AdvertisementTypeListSerializer

class AdvertisementSubTypeListSerializer(serializers.ModelSerializer):
    advertisement_type = AdvertisementTypeListSerializer(many="False", source='get_advertisement_type')
    class Meta:
        model = AdvertisementSubTypeTbl
        fields = ('name', 'id_string','is_active','created_by','created_date','advertisement_type')


class AdvertisementSubTypeViewSerializer(serializers.ModelSerializer):

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = AdvertisementSubTypeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')

class AdvertisementSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field Advertisement Type is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    adv_type_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = AdvertisementSubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_advertisement_subtype_validated_data(validated_data)
            if AdvertisementSubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                        utility_id=validated_data['utility_id'], adv_type_id=validated_data['adv_type_id']).exists():
                raise CustomAPIException(ADVERTISEMENT_SUBTYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                
                advertisement_subtype_obj = super(AdvertisementSubTypeSerializer, self).create(validated_data)
                advertisement_subtype_obj.created_by = user.id
                advertisement_subtype_obj.updated_by = user.id
                advertisement_subtype_obj.save()
                return advertisement_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_advertisement_subtype_validated_data(validated_data)
        with transaction.atomic():
            advertisement_subtype_obj = super(AdvertisementSubTypeSerializer, self).update(instance, validated_data)
            advertisement_subtype_obj.tenant = user.tenant
            advertisement_subtype_obj.updated_by = user.id
            advertisement_subtype_obj.updated_date = datetime.utcnow()
            advertisement_subtype_obj.save()
            return advertisement_subtype_obj