__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.meter_data_management.models.consumer_meter import ConsumerMeter as ConsumerMeterTbl
from v1.meter_data_management.serializers.consumer_meter import ConsumerMeterViewSerializer
from v1.meter_data_management.models.meter import get_meter_by_id_string


# API Header
# API end Point: api/v1/consumer-meter/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: consumer meter list
# Usage: API will fetch required data for consumer meter list against filter and search
# Tables used: LifeCycle
# Author: Akshay
# Created on: 18/02/2021

class ConsumerMeterList(generics.ListAPIView):
    try:
        serializer_class = ConsumerMeterViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'consumer_id', 'meter_id')
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',)  # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1, 1, 1, user_obj):
                    self.request.query_params._mutable = True
                    if 'consumer_id' in self.request.query_params:
                        self.request.query_params['consumer_id'] = get_consumer_by_id_string(self.request.query_params['consumer_id']).id
                    if 'meter_id' in self.request.query_params:
                        self.request.query_params['meter_id'] = get_meter_by_id_string(self.request.query_params['meter_id']).id
                    self.request.query_params._mutable = False
                    queryset = ConsumerMeterTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException
