__author__ = "aki"

from rest_framework import serializers, status
from v1.supplier.models.product_category import ProductCategory as ProductCategoryTbl
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NAME_ALREADY_EXIST
from v1.supplier.views.common_functions import set_product_category_vaidated_data

class ProductCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategoryTbl
        fields = ('id_string', 'name','is_active','created_by','created_date')

class ProductCategoryViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ProductCategoryTbl
        fields = ('id_string', 'name', 'tenant','tenant_id_string','utility','utility_id_string')

class ProductCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ProductCategoryTbl
        fields = ('__all__')

    def create(self, validated_data,  user):
        with transaction.atomic():
            validated_data = set_product_category_vaidated_data(validated_data)
            if ProductCategoryTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                product_category_obj = super(ProductCategorySerializer, self).create(validated_data)
                product_category_obj.created_by = user.id
                product_category_obj.updated_by = user.id
                product_category_obj.save()
                return product_category_obj

    def update(self, instance, validated_data, user):
        validated_data = set_product_category_vaidated_data(validated_data)
        if ProductCategoryTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                product_category_obj = super(ProductCategorySerializer, self).update(instance, validated_data)
                product_category_obj.updated_by = user.id
                product_category_obj.updated_date = datetime.utcnow()
                product_category_obj.save()
                return product_category_obj
