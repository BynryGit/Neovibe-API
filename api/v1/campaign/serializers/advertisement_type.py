from rest_framework import serializers, status
from v1.campaign.models.advertisement_type import AdvertisementType as AdvertisementTypeTbl
from api.settings import DISPLAY_DATE_TIME_FORMAT
from django.db import transaction
from datetime import datetime
from api.messages import ADVERTISEMENT_TYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.campaign.views.common_functions import set_advertisement_type_validated_data

class AdvertisementTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementTypeTbl
        fields = ('name', 'id_string','is_active','created_by','created_date')


class AdvertisementTypeViewSerializer(serializers.ModelSerializer):

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = AdvertisementTypeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')

class AdvertisementTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field Advertisement Type is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = AdvertisementTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_advertisement_type_validated_data(validated_data)
            if AdvertisementTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                        utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(ADVERTISEMENT_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                
                advertisement_type_obj = super(AdvertisementTypeSerializer, self).create(validated_data)
                advertisement_type_obj.created_by = user.id
                advertisement_type_obj.updated_by = user.id
                advertisement_type_obj.save()
                return advertisement_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_advertisement_type_validated_data(validated_data)
        with transaction.atomic():
            advertisement_type_obj = super(AdvertisementTypeSerializer, self).update(instance, validated_data)
            advertisement_type_obj.tenant = user.tenant
            advertisement_type_obj.updated_by = user.id
            advertisement_type_obj.updated_date = datetime.utcnow()
            advertisement_type_obj.save()
            return advertisement_type_obj

