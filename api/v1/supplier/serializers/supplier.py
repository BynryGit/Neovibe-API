__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.city import CitySerializer
from v1.commonapp.serializers.country import CountrySerializer
from v1.commonapp.serializers.state import StateSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier import Supplier as SupplierTbl
from v1.supplier.views.common_functions import set_supplier_validated_data


class SupplierViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    country = CountrySerializer()
    state = StateSerializer()
    city = CitySerializer()
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = SupplierTbl
        fields = ('id_string', 'name', 'description', 'phone_no', 'email_id', 'address_line_1', 'created_date',
                  'updated_date', 'tenant', 'utility', 'country', 'state', 'city')


class SupplierSerializer(serializers.ModelSerializer):
    tenant = serializers.UUIDField(required=True, source='tenant')
    utility = serializers.UUIDField(required=True, source='utility')
    country_id = serializers.IntegerField(required=False)
    state_id = serializers.IntegerField(required=False)
    city_id = serializers.IntegerField(required=False)
    source = serializers.IntegerField(required=False)
    status = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True, max_length=500)
    description = serializers.CharField(required=True, max_length=500)
    email_id = serializers.CharField(required=False, max_length=500)
    address_line_1 = serializers.CharField(required=False, max_length=500)

    class Meta:
        model = SupplierTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_supplier_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(SupplierSerializer, self).create(validated_data)
            utility_obj.created_by = user.id
            utility_obj.save()
            return utility_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(SupplierSerializer, self).update(instance, validated_data)
            utility_obj.updated_by = user.id
            utility_obj.updated_date = timezone.now()
            utility_obj.save()
            return utility_obj