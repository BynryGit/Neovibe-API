__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_status import UtilityStatus as UtilityStatusTbl
from v1.utility.serializers.status import UtilityStatusViewSerializer


# API Header
# API end Point: api/v1/utility/status/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Utility status list
# Usage: API will fetch required data for utility status list against filter and search
# Tables used: UtilityStatus
# Author: Akshay
# Created on: 20/05/2020

class UtilityStatusList(generics.ListAPIView):
    try:
        serializer_class = UtilityStatusViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('status',)
        ordering_fields = ('status',)
        ordering = ('status',) # always give by default alphabetical order
        search_fields = ('status',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = UtilityStatusTbl.objects.filter(utility__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/STATUS')
        raise APIException