__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.contract.models.contract_period import ContractPeriod as ContractPeriodTbl
from v1.contract.serializers.contract_period import ContractPeriodViewSerializer


# API Header
# API end Point: api/v1/contract/period/list
# API verb: GET
# Package: Basic
# Modules: Contract
# Sub Module: Period
# Interaction: Get contract period list
# Usage: API will fetch required data for contract period list.
# Tables used: 2.12.68 Contract Period
# Author: Akshay
# Created on: 29/05/2020


class ContractperiodList(generics.ListAPIView):
    try:
        serializer_class = ContractPeriodViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('id_string',)
        ordering_fields = ('period',)
        ordering = ('period',) # always give by default alphabetical order
        search_fields = ('period',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = ContractPeriodTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException