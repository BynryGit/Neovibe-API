__author__ = "aki"

from rest_framework import serializers
from v1.supplier.models.product_category import ProductCategory as ProductCategoryTbl


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategoryTbl
        fields = ('id_string', 'name')