__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_service import SupplierService as SupplierServiceTbl
from v1.supplier.views.common_functions import set_supplier_service_validated_data


class SupplierServiceViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)

    class Meta:
        model = SupplierServiceTbl
        fields = ('__all__')


class SupplierServiceSerializer(serializers.ModelSerializer):
    tenant = serializers.UUIDField(required=True, source='tenant')
    utility = serializers.UUIDField(required=True, source='utility')
    supplier = serializers.IntegerField(required=False)

    class Meta:
        model = SupplierServiceTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_supplier_service_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(SupplierServiceSerializer, self).create(validated_data)
            utility_obj.created_by = user.id
            utility_obj.save()
            return utility_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_service_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(SupplierServiceSerializer, self).update(instance, validated_data)
            utility_obj.updated_by = user.id
            utility_obj.updated_date = timezone.now()
            utility_obj.save()
            return utility_obj