__author__ = "priyanka"

from rest_framework import serializers
from v1.commonapp.models.products import Product as ProductTbl


class ProductViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductTbl
        fields = ('id_string', 'name','is_active')