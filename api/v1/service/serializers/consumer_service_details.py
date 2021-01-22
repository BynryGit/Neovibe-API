from datetime import datetime
from django.db import transaction
from rest_framework import serializers, status

from api.messages import CONSUMER_SERVICE_ALREADY_EXISTS
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.service.models.consumer_service_details import ServiceDetails
from v1.service.views.common_functions import generate_service_no, set_service_validated_data


class ServiceDetailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceDetails
        fields = ('name', 'id_string', 'request_date','created_by','is_active','state','consumer_no','service_request_no')


class ServiceDetailViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ServiceDetails
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    consumer_service_master_id = serializers.CharField(required=False, max_length=200)
    service_type_id = serializers.CharField(required=False, max_length=200)
    service_sub_type_id = serializers.CharField(required=False, max_length=200)
    service_status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ServiceDetails
        fields = '__all__'

    def create(self, validated_data, consumer, user):
        validated_data = set_service_validated_data(validated_data)
        if ServiceDetails.objects.filter(consumer_no=consumer.consumer_no, consumer_service_master_id=validated_data['consumer_service_master_id']).exists():
            raise CustomAPIException(CONSUMER_SERVICE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            service = super(ServiceSerializer, self).create(validated_data)
            # service.service_no = generate_service_no(service)
            service.created_by = user.id
            service.created_date = datetime.utcnow()
            service.save()
        return service

    def update(self, instance, validated_data, user):
        validated_data = set_service_validated_data(validated_data)
        with transaction.atomic():
            service = super(ServiceSerializer, self).update(instance, validated_data)
            service.updated_by = user.id
            service.updated_date = datetime.utcnow()
            service.save()
            return service