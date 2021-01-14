__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_product import SupplierProduct as SupplierProductTbl
from v1.supplier.serializers.product_category import ProductCategoryListSerializer
from v1.supplier.serializers.product_subcategory import ProductSubCategoryListSerializer
from v1.supplier.serializers.supplier import SupplierShortViewSerializer
from v1.supplier.views.common_functions import set_supplier_product_validated_data


class SupplierProductViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    supplier = SupplierShortViewSerializer(many=False, required=False, source='get_supplier')
    product_category = ProductCategoryListSerializer(many=False, required=False, source='get_product_category')
    product_subcategory = ProductSubCategoryListSerializer(many=False, required=False, source='get_product_subcategory')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = SupplierProductTbl
        fields = ('id_string', 'name', 'image', 'rate', 'quantity', 'unit', 'created_date', 'updated_date', 'tenant',
                  'utility', 'supplier', 'type', 'product_category', 'product_subcategory', 'status', 'source_type')


class SupplierProductSerializer(serializers.ModelSerializer):
    product_category = serializers.UUIDField(required=True)
    product_subcategory = serializers.UUIDField(required=True)
    type = serializers.UUIDField(required=False)
    status = serializers.UUIDField(required=False)
    source_type = serializers.UUIDField(required=False)
    name = serializers.CharField(required=True, max_length=200)
    rate = serializers.FloatField(required=True)
    quantity = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = SupplierProductTbl
        fields = ('__all__')

    def create(self, validated_data, supplier_obj, user):
        validated_data = set_supplier_product_validated_data(validated_data)
        if SupplierProductTbl.objects.filter(tenant=user.tenant, utility=user.utility,
                                             supplier=supplier_obj.id, name=validated_data["name"]).exists():
            return False
        with transaction.atomic():
            supplier_product_obj = super(SupplierProductSerializer, self).create(validated_data)
            supplier_product_obj.tenant = user.tenant
            supplier_product_obj.utility = user.utility
            supplier_product_obj.supplier = supplier_obj.id
            supplier_product_obj.created_by = user.id
            supplier_product_obj.save()
            return supplier_product_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_product_validated_data(validated_data)
        with transaction.atomic():
            supplier_product_obj = super(SupplierProductSerializer, self).update(instance, validated_data)
            supplier_product_obj.tenant = user.tenant
            supplier_product_obj.utility = user.utility
            supplier_product_obj.updated_by = user.id
            supplier_product_obj.updated_date = timezone.now()
            supplier_product_obj.save()
            return supplier_product_obj