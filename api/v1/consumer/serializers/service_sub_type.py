from rest_framework import serializers
from v1.consumer.models.service_sub_type import ServiceSubType as ServiceSubTypeTbl
from api.settings import DISPLAY_DATE_TIME_FORMAT
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import SERVICE_SUBTYPE_ALREADY_EXIST
from v1.consumer.views.common_functions import set_service_subtype_validated_data
from rest_framework import status
from v1.consumer.serializers.service_type import ServiceTypeListSerializer

class ServiceSubTypeListSerializer(serializers.ModelSerializer):
    service_type = ServiceTypeListSerializer(many="False",source="get_service_type")
    class Meta:
        model = ServiceSubTypeTbl
        fields = ('name', 'id_string','created_date','is_active','created_by','service_type')

class ServiceSubTypeViewSerializer(serializers.ModelSerializer):
    

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = ServiceSubTypeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')

class ServiceSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    service_type_id = serializers.CharField(required=True, max_length=200)
    

    class Meta:
        model = ServiceSubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_service_subtype_validated_data(validated_data)
            if ServiceSubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(SERVICE_SUBTYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                service_subtype_obj = super(ServiceSubTypeSerializer, self).create(validated_data)
                service_subtype_obj.created_by = user.id
                service_subtype_obj.updated_by = user.id
                service_subtype_obj.save()
                return service_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_service_subtype_validated_data(validated_data)
        with transaction.atomic():
            service_subtype_obj = super(ServiceSubTypeSerializer, self).update(instance, validated_data)
            service_subtype_obj.updated_by = user.id
            service_subtype_obj.updated_date = datetime.utcnow()
            service_subtype_obj.save()
            return service_subtype_obj