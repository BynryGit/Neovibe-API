from rest_framework import serializers, status
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from v1.commonapp.models.service_sub_type import ServiceSubTypes as ServiceSubTypeTbl
from django.db import transaction
from datetime import datetime
from api.messages import SERVICE_SUBTYPE_ALREADY_EXIST
from v1.commonapp.common_functions import set_service_subtype_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.serializers.service_type import ServiceTypeListSerializer

class ServiceSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ServiceSubTypeTbl
        fields = '__all__'


class ServiceSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field Service Sub Type name is required."})
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
            service_subtype_obj.tenant = user.tenant
            service_subtype_obj.updated_by = user.id
            service_subtype_obj.updated_date = datetime.utcnow()
            service_subtype_obj.save()
            return service_subtype_obj


class ServiceSubTypeListSerializer(serializers.ModelSerializer):
    service = ServiceTypeListSerializer(source='service_type')

    class Meta:
        model = ServiceSubTypeTbl
        fields = ('name', 'id_string','is_active','created_by','created_date','service')


class ServiceSubTypeShortListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceSubTypeTbl
        fields = ('name', 'id_string')