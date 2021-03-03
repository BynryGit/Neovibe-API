
from v1.consumer.models.offer_sub_type import OfferSubType as OfferSubTypeTbl
from v1.consumer.serializers.offer_type import OfferTypeListSerializer
from rest_framework import serializers, status
from api.messages import OFFER_SUB_TYPE_ALREADY_EXISTS
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.views.common_functions import set_offer_subtype_validated_data


class OfferSubTypeListSerializer(serializers.ModelSerializer):
    offer_type = OfferTypeListSerializer(source='get_offer_type')

    class Meta:
        model = OfferSubTypeTbl
        fields = ('name', 'id_string', 'offer_type', 'created_date', 'is_active', 'created_by')


class OfferSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = OfferSubTypeTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class OfferSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    offer_type_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = OfferSubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_offer_subtype_validated_data(validated_data)
            if OfferSubTypeTbl.objects.filter(name=validated_data['name'],
                                              tenant_id=validated_data['tenant_id'],
                                              utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(OFFER_SUB_TYPE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
            else:
                offer_subtype_obj = super(OfferSubTypeSerializer, self).create(validated_data)
                offer_subtype_obj.created_by = user.id
                offer_subtype_obj.save()
                return offer_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_offer_subtype_validated_data(validated_data)
        with transaction.atomic():
            offer_subtype_obj = super(OfferSubTypeSerializer, self).update(instance, validated_data)
            offer_subtype_obj.updated_by = user.id
            offer_subtype_obj.updated_date = datetime.utcnow()
            offer_subtype_obj.save()
            return offer_subtype_obj
