__author__ = "Priyanka"

from api.settings import DISPLAY_DATE_TIME_FORMAT,INPUT_DATE_FORMAT
from rest_framework import serializers
from datetime import datetime
from django.db import transaction
from v1.dispatcher.views.common_functions import set_validated_data
from v1.dispatcher.models.service_appointments import ServiceRequest
from v1.commonapp.serializers.service_type import ServiceTypeListSerializer
from v1.commonapp.serializers.city import CitySerializer
from v1.consumer.serializers.consumer_master import ConsumerViewSerializer
from v1.asset.serializer.asset import AssetViewSerializer
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.serializers.sub_area import SubAreaListSerializer
from v1.dispatcher.models.sop_status import SopStatus
from v1.consumer.models.consumer_master import ConsumerMaster
from v1.asset.models.asset_master import Asset

class SOPStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SopStatus
        fields = ('id_string','name')

class ConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerMaster
        fields = ('id_string','first_name')

class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ('id_string','name')



class ServiceRequestViewSerializer(serializers.ModelSerializer):


    service_type_id = ServiceTypeListSerializer(many=False, required=True, source='get_service_type')
    city_id = CitySerializer(many=False, required=True, source='get_city')
    consumer_id = ConsumerSerializer(many=False, required=True, source='get_consumer')
    asset_id = AssetSerializer(many=False, required=True, source='get_asset')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT,read_only=True)
    start_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT)
    end_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT)
    area_id = AreaListSerializer(many=False, required=True, source='get_area')
    sub_area_id = SubAreaListSerializer(many=False, required=True, source='get_sub_area')
    # status_id = SOPStatusSerializer(many=False, required=True, source='get_sop_status')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = ServiceRequest
        fields = ('id_string', 'tenant_name', 'service_name','asset_id','city_id','area_id','sub_area_id','service_type_id',
                  'consumer_id','city_id','start_date','end_date','created_date','is_active')

class ServiceRequestSerializer(serializers.ModelSerializer):
    service_type_id = serializers.CharField(required=False, max_length=200)
    service_name = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, max_length=200)
    consumer_id = serializers.CharField(required=False, max_length=200)
    consumer_address = serializers.CharField(required=False, max_length=200)
    asset_id = serializers.CharField(required=False, max_length=200)
    duration = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    start_date = serializers.DateTimeField(required=False,format="%d-%m-%Y")
    end_date = serializers.DateTimeField(required=False,format="%d-%m-%Y")
    status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
            model = ServiceRequest
            fields = ('__all__')

    def create(self, validated_data, user,asset_obj):
        validated_data = set_validated_data(validated_data)
        if ServiceRequest.objects.filter(**validated_data).exists():
            return False
        else:
            with transaction.atomic():
                service_request_obj = super(ServiceRequestSerializer, self).create(validated_data)
                service_request_obj.asset_no = asset_obj.id
                service_request_obj.created_by = user.id
                # service_request_obj.created_date = datetime.now()
                service_request_obj.tenant = user.tenant
                service_request_obj.utility = user.utility
                service_request_obj.save()
                service_request_obj.service_no = str(service_request_obj.service_name)+str(service_request_obj.tenant)+str(service_request_obj.utility)
                service_request_obj.is_active = True
                service_request_obj.save()
                return service_request_obj

    def update(self, instance, validated_data, user):
            validated_data = set_validated_data(validated_data)
            with transaction.atomic():
                service_request_obj = super(ServiceRequestSerializer, self).update(instance, validated_data)
                service_request_obj.updated_by = user.id
                # service_request_obj.updated_date = datetime.now()
                service_request_obj.save()
                return service_request_obj

