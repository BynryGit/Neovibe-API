__author__ = "aki"

from rest_framework import serializers
from v1.supplier.models.product_subcategory import ProductSubCategory as ProductSubCategoryTbl


class ProductSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSubCategoryTbl
        fields = ('id_string', 'name')