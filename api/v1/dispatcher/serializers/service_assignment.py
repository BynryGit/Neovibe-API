__author__ = "Priyanka"

from api.settings import DISPLAY_DATE_TIME_FORMAT
from rest_framework import serializers
from datetime import datetime
from django.db import transaction
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.serializers.service_type import ServiceTypeListSerializer
from v1.commonapp.serializers.city import CitySerializer
from v1.dispatcher.models.sop_status import SopStatus
from v1.dispatcher.models.service_appointments import ServiceRequest
from v1.supplier.models.supplier import Supplier
from v1.dispatcher.models.service_assignment import ServiceAssignment
from v1.dispatcher.views.common_functions import set_validated_data

class SOPStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SopStatus
        fields = ('id_string','name')

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ('id_string','service_name')

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id_string','name')

class ServiceAssignmentViewSerializer(serializers.ModelSerializer):

    service_request_id = ServiceRequestSerializer(many=False, required=True, source='get_service_request')
    service_type_id = ServiceTypeListSerializer(many=False, required=True, source='get_service_type')
    city_id = CitySerializer(many=False, required=True, source='get_city')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT,read_only=True)
    area_id = AreaListSerializer(many=False, required=True, source='get_area')
    status_id = SOPStatusSerializer(many=False, required=True, source='get_sop_status')
    vendor_id = VendorSerializer(many=False, required=True, source='get_vendor')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    completion_date =serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT)
    assigned_date =serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT)
    start_date =serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT)


    class Meta:
        model = ServiceAssignment
        fields = ('id_string', 'tenant_name','assigned_date','start_date','completion_date',
                  'defined_duration','actual_duration','service_request_id','service_type_id',
                  'vendor_id','city_id','area_id','status_id',
                  'is_active','created_date')


class ServiceAssignmentSerializer(serializers.ModelSerializer):
    assigned_date = serializers.DateTimeField(required=False,format="%d-%m-%Y")
    start_date = serializers.DateTimeField(required=False,format="%d-%m-%Y")
    completion_date = serializers.DateTimeField(required=False,format="%d-%m-%Y")
    defined_duration = serializers.CharField(required=False, max_length=200)
    actual_duration = serializers.CharField(required=False, max_length=200)
    service_request_id = serializers.CharField(required=False, max_length=200)
    service_type_id = serializers.CharField(required=False, max_length=200)
    vendor_id = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    is_complete_on_time = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ServiceAssignment
        fields =  ('__all__')

    def create(self, validated_data, user,asset_obj):
        validated_data = set_validated_data(validated_data)
        if ServiceAssignment.objects.filter(**validated_data).exists():
            return False
        else:
            with transaction.atomic():
                assign_obj = super(ServiceAssignmentSerializer, self).create(validated_data)
                assign_obj.asset_id = asset_obj.id
                assign_obj.created_by = user.id
                assign_obj.created_date = datetime.now()
                assign_obj.tenant = user.tenant
                assign_obj.utility = user.utility
                assign_obj.save()
                return assign_obj

    def update(self, instance, validated_data, user):
            validated_data = set_validated_data(validated_data)
            with transaction.atomic():
                assign_obj = super(ServiceAssignmentSerializer, self).update(instance, validated_data)
                assign_obj.updated_by = user.id
                assign_obj.updated_date = datetime.now()
                assign_obj.save()
                return assign_obj