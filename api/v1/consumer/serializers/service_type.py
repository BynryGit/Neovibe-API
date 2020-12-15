from rest_framework import serializers
from v1.consumer.models.service_type import ServiceType as ServiceTypeTbl
from api.settings import DISPLAY_DATE_TIME_FORMAT
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import SERVICE_TYPE_ALREADY_EXIST
from v1.consumer.views.common_functions import set_service_type_validated_data
from rest_framework import status

class ServiceTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTypeTbl
        fields = ('name', 'id_string','created_date','is_active','created_by')

class ServiceTypeViewSerializer(serializers.ModelSerializer):
    

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = ServiceTypeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')

class ServiceTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    

    class Meta:
        model = ServiceTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_service_type_validated_data(validated_data)
            if ServiceTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
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
            service_type_obj.updated_by = user.id
            service_type_obj.updated_date = datetime.utcnow()
            service_type_obj.save()
            return service_type_obj