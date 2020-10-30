__author__ = "priyanka"

from rest_framework.exceptions import APIException
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.models.products import Product as ProductTbl
from v1.commonapp.serializers.products import ProductViewSerializer


# API Header
# API end Point: api/v1/product/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction:  Product list
# Usage: API will fetch required data for ProductTbl list 
# Tables used: product
# Author: priyanka
# Created on: 16/10/2020

class ProductList(generics.ListAPIView):
    try:
        serializer_class = ProductViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name',)
        ordering_fields = ('name',)
        ordering = ('name',) # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = ProductTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException