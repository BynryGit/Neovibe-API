__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier import Supplier as SupplierTbl
from v1.supplier.views.common_functions import set_supplier_validated_data
from v1.tenant.serializers.tenant_city import TenantCitySerializer
from v1.tenant.serializers.tenant_country import TenantCountrySerializer
from v1.tenant.serializers.tenant_state import TenantStateSerializer


class SupplierViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    country_id = TenantCountrySerializer(many=False, required=False, source='get_tenant_country')
    state_id = TenantStateSerializer(many=False, required=False, source='get_tenant_state')
    city_id = TenantCitySerializer(many=False, required=False, source='get_tenant_city')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = SupplierTbl
        fields = ('id_string', 'name', 'description', 'phone_no', 'email_id', 'address_line_1', 'created_date',
                  'updated_date', 'tenant', 'utility', 'country_id', 'state_id', 'city_id')


class SupplierSerializer(serializers.ModelSerializer):
    country_id = serializers.UUIDField(required=False)
    state_id = serializers.UUIDField(required=False)
    city_id = serializers.UUIDField(required=False)
    source = serializers.UUIDField(required=False)
    status_id = serializers.UUIDField(required=False)
    name = serializers.CharField(required=True, max_length=500)
    description = serializers.CharField(required=True, max_length=500)
    email_id = serializers.CharField(required=False, max_length=500)
    address_line_1 = serializers.CharField(required=False, max_length=500)

    class Meta:
        model = SupplierTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_supplier_validated_data(validated_data)
        if SupplierTbl.objects.filter(tenant=user.tenant, utility=user.utility, name=validated_data["name"]).exists():
            return False
        with transaction.atomic():
            supplier_obj = super(SupplierSerializer, self).create(validated_data)
            supplier_obj.tenant = user.tenant
            supplier_obj.utility = user.utility
            supplier_obj.created_by = user.id
            supplier_obj.save()
            return supplier_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_validated_data(validated_data)
        with transaction.atomic():
            supplier_obj = super(SupplierSerializer, self).update(instance, validated_data)
            supplier_obj.tenant = user.tenant
            supplier_obj.utility = user.utility
            supplier_obj.updated_by = user.id
            supplier_obj.updated_date = timezone.now()
            supplier_obj.save()
            return supplier_obj