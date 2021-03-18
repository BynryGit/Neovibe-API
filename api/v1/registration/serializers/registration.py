from datetime import datetime
from django.db import transaction
from rest_framework import serializers, status
from api.messages import MOBILE_ALREADY_EXISTS
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.registration.models.registrations import Registration
from v1.registration.views.common_functions import generate_registration_no, \
    set_registration_validated_data


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]


class RegistrationListSerializer(serializers.ModelSerializer):
    # area = AreaListSerializer(many=False, source='get_area')
    state = ChoiceField(choices=Registration.CHOICES)
    billing_area = serializers.ReadOnlyField(source='get_area')

    class Meta:
        model = Registration
        fields = (
            'id_string', 'registration_no', 'email_id', 'phone_mobile', 'billing_address_line_1',
            'billing_street', 'billing_zipcode', 'state', 'billing_area', 'created_date')        
        # fields = (
        #     'id_string', 'registration_no', 'first_name', 'last_name', 'email_id', 'phone_mobile', 'address_line_1',
        #     'street', 'zipcode', 'state', 'area', 'created_date')


class RegistrationViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    billing_state = serializers.ReadOnlyField(source='get_state')
    billing_city = serializers.ReadOnlyField(source='get_city')
    billing_area = serializers.ReadOnlyField(source='get_area')
    billing_sub_area = serializers.ReadOnlyField(source='get_sub_area')
    premise = serializers.ReadOnlyField(source='get_premise')
    state = ChoiceField(choices=Registration.CHOICES)

    # def to_representation(self, instance):
    #     data = super(RegistrationViewSerializer, self).to_representation(instance)
    #     data['registration_date'] = instance.registration_date.strftime(setting_reader.get_display_date_format())
    #     return data

    class Meta:
        model = Registration
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'registration_no',
                  'email_id', 'phone_mobile', 'billing_address_line_1', 'billing_street',
                  'billing_zipcode', 'billing_state', 'billing_city', 'billing_area', 'billing_sub_area', 'premise',
                  'state')


class RegistrationSerializer(serializers.ModelSerializer):
    utility = serializers.CharField(required=False, max_length=200)
    phone_mobile = serializers.CharField(required=True, max_length=200)
    billing_state_id = serializers.CharField(required=False, max_length=200)
    billing_city_id = serializers.CharField(required=False, max_length=200)
    billing_area_id = serializers.CharField(required=False, max_length=200)
    billing_sub_area_id = serializers.CharField(required=False, max_length=200)
    ownership_id = serializers.CharField(required=False, max_length=200)
    premise_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Registration
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_registration_validated_data(validated_data)
            if Registration.objects.filter(phone_mobile=validated_data['phone_mobile'], tenant=user.tenant,
                                           utility_id=validated_data['utility']).exists():
                raise CustomAPIException(MOBILE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
            else:
                registration_obj = super(RegistrationSerializer, self).create(validated_data)
                registration_obj.created_by = user.id
                registration_obj.created_date = datetime.utcnow()
                registration_obj.tenant = user.tenant
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
