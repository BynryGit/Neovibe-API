__author__ = "chinmay"

from django.db import transaction
from django.utils import timezone
from api.messages import SMART_METER_CONFIGURATION_ALREADY_EXISTS
from rest_framework import serializers, status
from v1.commonapp.models.country import Country as CountryTbl
from api.messages import *
from django.db import transaction
from v1.commonapp.serializers.region import RegionSerializer, RegionListSerializer
from v1.utility.serializers.utility_product import UtilityProductListSerializer
from v1.meter_data_management.models.smart_meter_configuration import \
    SmartMeterConfiguration as SmartMeterConfigurationTbl, get_smart_meter_configuration_by_id_string
from v1.meter_data_management.views.common_function import set_smart_meter_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from datetime import datetime




class SmartMeterListSerializer(serializers.ModelSerializer):
    utility_product = UtilityProductListSerializer(source="get_utility_product")

    class Meta:
        model = SmartMeterConfigurationTbl
        fields = ('smart_meter_api_name', 'id_string', 'vendor_name','utility_product', 'created_date', 'is_active', 'created_by')


class SmartMeterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = SmartMeterConfigurationTbl
        fields = ('smart_meter_api_name', 'id_string', 'utility', 'utility_id_string', 'tenant', 'tenant_id_string')


class SmartMeterSerializer(serializers.ModelSerializer):
    utility_product_id = serializers.UUIDField(required=True)
    request_parameter = serializers.JSONField(required=False)
    utility_id = serializers.UUIDField(required=False)
    tenant_id = serializers.UUIDField(required=False)
    smart_meter_api_name = serializers.CharField(required=True, max_length=200,
                                                 error_messages={
                                                     "required": "The field smart meter api name is required."})

    class Meta:
        model = SmartMeterConfigurationTbl
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_smart_meter_validated_data(validated_data)
        if SmartMeterConfigurationTbl.objects.filter(tenant_id=validated_data['tenant_id'], utility_id=validated_data['utility_id'],
                                                     smart_meter_api_name=validated_data['smart_meter_api_name']).exists():
            raise CustomAPIException(SMART_METER_CONFIGURATION_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                smart_meter_obj = super(SmartMeterSerializer, self).create(validated_data)
                smart_meter_obj.tenant = user.tenant
                smart_meter_obj.created_by = user.id
                smart_meter_obj.save()
                return smart_meter_obj

    def update(self, instance, validated_data, user):
        validated_data = set_smart_meter_validated_data(validated_data)
        if SmartMeterConfigurationTbl.objects.filter(tenant_id=validated_data['tenant_id'], utility_id=validated_data['utility_id'],
                                                     smart_meter_api_name=validated_data['smart_meter_api_name']).exists():
            raise CustomAPIException(SMART_METER_CONFIGURATION_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                smart_meter_obj = super(SmartMeterSerializer, self).update(instance, validated_data)
                smart_meter_obj.tenant = user.tenant
                smart_meter_obj.updated_by = user.id
                smart_meter_obj.updated_date = timezone.now()
                smart_meter_obj.save()
                return smart_meter_obj
