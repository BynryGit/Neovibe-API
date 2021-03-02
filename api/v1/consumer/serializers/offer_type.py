from v1.consumer.models.offer_type import OfferType as OfferTypeTbl
from rest_framework import serializers, status
from api.messages import OFFER_TYPE_ALREADY_EXISTS
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.views.common_functions import set_offer_type_validated_data


class OfferTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferTypeTbl
        fields = ('name', 'id_string', 'created_date', 'is_active', 'created_by')


class OfferTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = OfferTypeTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class OfferTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = OfferTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_offer_type_validated_data(validated_data)
            if OfferTypeTbl.objects.filter(name=validated_data['name'],
                                           tenant_id=validated_data['tenant_id'],
                                           utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(OFFER_TYPE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
            else:
                offer_type_obj = super(OfferTypeSerializer, self).create(validated_data)
                offer_type_obj.created_by = user.id
                offer_type_obj.save()
                return offer_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_offer_type_validated_data(validated_data)
        with transaction.atomic():
            offer_type_obj = super(OfferTypeSerializer, self).update(instance, validated_data)
            offer_type_obj.updated_by = user.id
            offer_type_obj.updated_date = datetime.utcnow()
            offer_type_obj.save()
            return offer_type_obj
