__author__ = "aki"

from rest_framework import serializers, status
from v1.supplier.models.product_subcategory import ProductSubCategory as ProductSubCategoryTbl
from v1.supplier.serializers.product_category import ProductCategoryListSerializer
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NAME_ALREADY_EXIST
from v1.supplier.views.common_functions import set_product_subcategory_vaidated_data

class ProductSubCategoryListSerializer(serializers.ModelSerializer):
    product_category=ProductCategoryListSerializer(many=False, source='get_product_category')

    class Meta:
        model = ProductSubCategoryTbl
        fields = ('id_string', 'name','is_active','created_by','created_date','product_category')

class ProductSubCategoryViewSerializer(serializers.ModelSerializer):
    product_category=ProductCategoryListSerializer(many=False, source='get_product_category')
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ProductSubCategoryTbl
        fields = ('id_string', 'name', 'tenant','tenant_id_string','utility','utility_id_string','product_category')

class ProductSubCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    category=serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ProductSubCategoryTbl
        fields = ('__all__')

    def create(self, validated_data,  user):
        with transaction.atomic():
            validated_data = set_product_subcategory_vaidated_data(validated_data)
            if ProductSubCategoryTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                product_subcategory_obj = super(ProductSubCategorySerializer, self).create(validated_data)
                product_subcategory_obj.created_by = user.id
                product_subcategory_obj.updated_by = user.id
                product_subcategory_obj.save()
                return product_subcategory_obj

    def update(self, instance, validated_data, user):
        validated_data = set_product_subcategory_vaidated_data(validated_data)
        if ProductSubCategoryTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                product_subcategory_obj = super(ProductSubCategorySerializer, self).update(instance, validated_data)
                product_subcategory_obj.updated_by = user.id
                product_subcategory_obj.updated_date = datetime.utcnow()
                product_subcategory_obj.save()
                return product_subcategory_obj


