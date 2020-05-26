__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_product import SupplierProduct as SupplierProductTbl
from v1.supplier.views.common_functions import set_supplier_product_validated_data


class SupplierProductViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)

    class Meta:
        model = SupplierProductTbl
        fields = ('__all__')


class SupplierProductSerializer(serializers.ModelSerializer):
    tenant = serializers.UUIDField(required=True, source='tenant')
    utility = serializers.UUIDField(required=True, source='utility')
    supplier = serializers.IntegerField(required=False)
    product_category = serializers.IntegerField(required=False)
    product_subcategory = serializers.IntegerField(required=False)
    rate = serializers.FloatField(required=True)
    quantity = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = SupplierProductTbl
        fields = ('__all__')

    def create(self, validated_data, supplier_obj, user):
        validated_data = set_supplier_product_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(SupplierProductSerializer, self).create(validated_data)
            utility_obj.created_by = user.id
            utility_obj.save()
            return utility_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_product_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(SupplierProductSerializer, self).update(instance, validated_data)
            utility_obj.updated_by = user.id
            utility_obj.updated_date = timezone.now()
            utility_obj.save()
            return utility_obj