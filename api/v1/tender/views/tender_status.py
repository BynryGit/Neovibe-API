__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tender.serializers.tender_status import TenderStatusViewSerializer
from v1.tender.models.tender_status import TenderStatus as TenderStatusTbl


# API Header
# API end Point: api/v1/tender/status/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tender status list
# Usage: API will fetch required data for tender status list against filter and search
# Tables used: 2.12.89 Tender Status
# Author: Akshay
# Created on: 09/06/2020


class TenderStatusList(generics.ListAPIView):
    try:
        serializer_class = TenderStatusViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('id_string',)
        ordering_fields = ('status',)
        ordering = ('status',) # always give by default alphabetical order
        search_fields = ('status',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = TenderStatusTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException