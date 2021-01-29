from rest_framework import serializers
from v1.registration.models.registration_subtype import RegistrationSubType as RegistrationSubTypeTbl
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import REGISTRATION_SUBTYPE_ALREADY_EXIST
from v1.registration.views.common_functions import set_registration_subtype_validated_data
from rest_framework import status
from v1.registration.serializers.registration_type import RegistrationTypeListSerializer

class RegistrationSubTypeListSerializer(serializers.ModelSerializer):
    registration_type = RegistrationTypeListSerializer(many="False", source='get_registration_type')
    class Meta: 
        model = RegistrationSubTypeTbl
        fields = ('name', 'id_string','registration_type','created_date','is_active','created_by')

class RegistrationSubTypeViewSerializer(serializers.ModelSerializer):
    

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = RegistrationSubTypeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')

class RegistrationSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    registration_type_id = serializers.CharField(required=True, max_length=200)
    

    class Meta:
        model = RegistrationSubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_registration_subtype_validated_data(validated_data)
            if RegistrationSubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(REGISTRATION_SUBTYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                registration_subtype_obj = super(RegistrationSubTypeSerializer, self).create(validated_data)
                registration_subtype_obj.created_by = user.id
                registration_subtype_obj.updated_by = user.id
                registration_subtype_obj.save()
                return registration_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_registration_subtype_validated_data(validated_data)
        with transaction.atomic():
            registration_subtype_obj = super(RegistrationSubTypeSerializer, self).update(instance, validated_data)
            registration_subtype_obj.updated_by = user.id
            registration_subtype_obj.updated_date = datetime.utcnow()
            registration_subtype_obj.save()
            return registration_subtype_obj