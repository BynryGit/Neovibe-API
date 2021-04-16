__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.meter_make import MeterMake as MeterMakeTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.meter_data_management.serializers.meter_make import MeterMakeViewSerializer


# API Header
# API end Point: api/v1/meter-data/meter-make/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter make list
# Usage: API will fetch required data for meter make list against filter and search
# Tables used: MeterMake
# Author: Akshay
# Created on: 19/02/2021


class MeterMakeList(generics.ListAPIView):
    try:
        serializer_class = MeterMakeViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string',)
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    queryset = MeterMakeTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='MX', sub_module='METER_MASTER')
        raise APIException
