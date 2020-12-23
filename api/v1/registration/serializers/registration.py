from datetime import datetime
from django.db import transaction
from rest_framework import serializers, status
import os
# if os.environ['smart360_env'] == 'dev':
#     from api.settings_dev import *
# else:
from api.settings import *
from api.messages import MOBILE_ALREADY_EXISTS
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.serializers.consumer_category import ConsumerCategoryViewSerializer
from v1.consumer.serializers.consumer_sub_category import ConsumerSubCategoryViewSerializer
from v1.registration.models.registrations import Registration
from v1.registration.views.common_functions import generate_registration_no, \
    set_registration_validated_data


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]


class RegistrationListSerializer(serializers.ModelSerializer):
    area = AreaListSerializer(many=False, source='get_area')

    class Meta:
        model = Registration
        fields = (
            'id_string', 'registration_no', 'first_name', 'last_name', 'email_id', 'phone_mobile', 'address_line_1',
            'street', 'zipcode', 'state', 'area', 'created_date')


class RegistrationViewSerializer(serializers.ModelSerializer):
    area = AreaListSerializer(many=False, source='get_area')
    category = ConsumerCategoryViewSerializer(many=False, source='get_consumer_category')
    sub_category = ConsumerSubCategoryViewSerializer(many=False, source='get_consumer_sub_category')
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    state = ChoiceField(choices=Registration.CHOICES)

    def to_representation(self, instance):
        data = super(RegistrationViewSerializer, self).to_representation(instance)
        data['registration_date'] = instance.registration_date.strftime(DISPLAY_DATE_TIME_FORMAT)
        return data

    class Meta:
        model = Registration
        fields = (
            'id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'registration_no', 'first_name',
            'last_name', 'email_id', 'phone_mobile', 'address_line_1', 'street', 'zipcode', 'registration_date',
            'state', 'area', 'category', 'sub_category', 'created_date', 'billing_address_line_1')


class RegistrationSerializer(serializers.ModelSerializer):
    phone_mobile = serializers.CharField(required=True, max_length=200,
                                         error_messages={"required": "The field phone_mobile is required."})
    area_id = serializers.CharField(required=False, max_length=200)
    billing_area_id = serializers.CharField(required=False, max_length=200)
    utility_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    registration_type_id = serializers.CharField(required=False, max_length=200)
    country_id = serializers.CharField(required=False, max_length=200)
    state_id = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    billing_state_id = serializers.CharField(required=False, max_length=200)
    billing_city_id = serializers.CharField(required=False, max_length=200)
    scheme_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    billing_sub_area_id = serializers.CharField(required=False, max_length=200)
    payment_id = serializers.CharField(required=False, max_length=200)
    ownership_id = serializers.CharField(required=False, max_length=200)
    consumer_category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    source_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Registration
        fields = ('__all__')

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_registration_validated_data(validated_data)
            if Registration.objects.filter(phone_mobile=validated_data['phone_mobile'], tenant=user.tenant,
                                           utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(MOBILE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
            else:
                registration_obj = super(RegistrationSerializer, self).create(validated_data)
                registration_obj.created_by = user.id
                registration_obj.created_date = datetime.utcnow()
                registration_obj.tenant = user.tenant
                registration_obj.registration_no = generate_registration_no(registration_obj)
                registration_obj.save()
                return registration_obj

    def update(self, instance, validated_data, user):
        validated_data = set_registration_validated_data(validated_data)
        if Registration.objects.exclude(id_string=instance.id_string).filter(
                phone_mobile=validated_data['phone_mobile'], tenant=user.tenant, utility=instance.utility).exists():
            raise CustomAPIException(MOBILE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                registration_obj = super(RegistrationSerializer, self).update(instance, validated_data)
                registration_obj.updated_by = user.id
                registration_obj.updated_date = datetime.utcnow()
                registration_obj.save()
                return registration_obj
