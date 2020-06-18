__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tender.models.tender_type import TenderType as TenderTypeTbl
from v1.tender.serializers.tender_type import TenderTypeViewSerializer


# API Header
# API end Point: api/v1/tender/type/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tender type list
# Usage: API will fetch required data for tender type list against filter and search
# Tables used: Tender Type
# Author: Akshay
# Created on: 09/06/2020


class TenderTypeList(generics.ListAPIView):
    try:
        serializer_class = TenderTypeViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('id_string',)
        ordering_fields = ('type',)
        ordering = ('type',) # always give by default alphabetical order
        search_fields = ('type',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = TenderTypeTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException
