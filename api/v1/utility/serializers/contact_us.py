from rest_framework import serializers
from v1.utility.models.contact_us import ContactUs as ContactUsTbl
from v1.commonapp.views.settings_reader import SettingReader

setting_reader = SettingReader()
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import CONTACT_DATA_WITH_EMAIL_ALREADY_EXIST
from v1.utility.views.common_functions import set_contact_us_validated_data
from rest_framework import status


class ContactUsListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ContactUsTbl
        fields = ('tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'email', "emergency_no",
                  "working_days", "portal_site")


class ContactUsViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ContactUsTbl
        fields = (
            'id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')


class ContactUsSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, max_length=200,
                                  error_messages={"required": "The field Email is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ContactUsTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_contact_us_validated_data(validated_data)
            if ContactUsTbl.objects.filter(email=validated_data['email'], tenant_id=validated_data['tenant_id'],
                                           utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(CONTACT_DATA_WITH_EMAIL_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                contact_us_obj = super(ContactUsSerializer, self).create(validated_data)
                contact_us_obj.created_by = user.id
                contact_us_obj.save()
                return contact_us_obj

    def update(self, instance, validated_data, user):
        validated_data = set_contact_us_validated_data(validated_data)
        if ContactUsTbl.objects.filter(email=validated_data['email'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(CONTACT_DATA_WITH_EMAIL_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                contact_us_obj = super(ContactUsSerializer, self).update(instance, validated_data)
                contact_us_obj.updated_by = user.id
                contact_us_obj.updated_date = datetime.utcnow()
                contact_us_obj.save()
                return contact_us_obj
