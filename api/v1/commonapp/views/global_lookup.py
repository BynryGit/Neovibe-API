__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from v1.commonapp.views.logger import logger
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.models.global_lookup import Global_Lookup as Global_LookupTbl
from v1.commonapp.serializers.global_lookup import GlobalLookupViewSerializer
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException


# API Header
# API end Point: api/v1/global-lookup/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Global Lookup list
# Usage: API will fetch required data for global lookup list against filter and search
# Tables used: Global Lookup
# Author: Akshay
# Created on: 11/01/2021

class Global_LookupList(generics.ListAPIView):
    try:
        serializer_class = GlobalLookupViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('category',)
        ordering_fields = ('category',)
        ordering = ('category',) # always give by default alphabetical order
        search_fields = ('category',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    queryset = Global_LookupTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException