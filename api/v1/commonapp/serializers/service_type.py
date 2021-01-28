__author__ = "Arpita"

from rest_framework import serializers, status
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.models.service_type import ServiceType
from django.db import transaction
from datetime import datetime
from api.messages import SERVICE_TYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_service_type_validated_data



class GetServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = ('name', 'id_string')


class ServiceTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = ('name', 'id_string','is_active','created_by','created_date')


class ServiceTypeViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(setting_reader.get_display_date_format())

    created_date = serializers.SerializerMethodField('get_created_date')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    class Meta:
        model = ServiceType
        fields = ('id_string', 'tenant_name', 'name','created_date','is_active','tenant','tenant_id_string','utility','utility_id_string')


class ServiceTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field Service Type name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ServiceType
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_service_type_validated_data(validated_data)
            if ServiceType.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                        utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(SERVICE_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                
                service_type_obj = super(ServiceTypeSerializer, self).create(validated_data)
                service_type_obj.created_by = user.id
                service_type_obj.updated_by = user.id
                service_type_obj.save()
                return service_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_service_type_validated_data(validated_data)
        with transaction.atomic():
            service_type_obj = super(ServiceTypeSerializer, self).update(instance, validated_data)
            service_type_obj.tenant = user.tenant
            service_type_obj.updated_by = user.id
            service_type_obj.updated_date = datetime.utcnow()
            service_type_obj.save()
            return service_type_obj