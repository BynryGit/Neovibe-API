__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.contract.models.contract_status import ContractStatus as ContractStatusTbl
from v1.contract.serializers.contract_status import ContractStatusViewSerializer


# API Header
# API end Point: api/v1/contract/status/list
# API verb: GET
# Package: Basic
# Modules: Contract
# Sub Module: Status
# Interaction: Get contract status list
# Usage: API will fetch required data for contract status list.
# Tables used: Contract Status
# Author: Akshay
# Created on: 29/05/2020


class ContractStatusList(generics.ListAPIView):
    try:
        serializer_class = ContractStatusViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('id_string',)
        ordering_fields = ('name',)
        ordering = ('name',) # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = ContractStatusTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException