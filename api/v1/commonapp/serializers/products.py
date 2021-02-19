__author__ = "priyanka"

from rest_framework import serializers, status
from v1.commonapp.models.products import Product as ProductTbl
from django.db import transaction
from v1.commonapp.common_functions import set_product_validated_data
from datetime import datetime
from api.messages import PRODUCT_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_product import UtilityProduct as UtilityProductTbl


class ProductViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityProductTbl
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    product_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityProductTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_product_validated_data(validated_data)
            if UtilityProductTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(PRODUCT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:

                product_obj = super(ProductSerializer, self).create(validated_data)
                product_obj.created_by = user.id
                product_obj.created_date = datetime.utcnow()
                product_obj.save()
                return product_obj

    def update(self, instance, validated_data, user):
        validated_data = set_product_validated_data(validated_data)
        with transaction.atomic():
            product_obj = super(ProductSerializer, self).update(instance, validated_data)
            product_obj.tenant = user.tenant
            product_obj.updated_by = user.id
            product_obj.updated_date = datetime.utcnow()
            product_obj.save()
            return product_obj


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTbl
        fields = ('name', 'id_string', 'is_active', 'created_by', 'created_date')
