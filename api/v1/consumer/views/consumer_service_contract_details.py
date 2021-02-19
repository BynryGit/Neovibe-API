from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.models.consumer_service_contract_details import ConsumerServiceContractDetail
from v1.consumer.serializers.consumer_service_contract_details import ConsumerServiceContractDetailViewSerializer
from v1.meter_data_management.models.meter import get_meter_by_id_string


class ConsumerServiceContractDetailList(generics.ListAPIView):
    try:
        serializer_class = ConsumerServiceContractDetailViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    consumer = get_consumer_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerServiceContractDetail.objects.filter(consumer_id=consumer.id, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer service contracts not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer ops', sub_module='consumer')

# Note: rohan below is updated api for fetch service contract detail list you just delete above code give class name to below api and delete url


# API Header
# API end Point: api/v1/service-contract-detail/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: consumer service contract detail list
# Usage: API will fetch required data for consumer service contract detail list against filter and search
# Tables used: ConsumerServiceContractDetail
# Author: Akshay
# Created on: 19/02/2021

class ConsumerMeterList(generics.ListAPIView):
    try:
        serializer_class = ConsumerServiceContractDetailViewSerializer
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
                        self.request.query_params['consumer_id'] = get_consumer_by_id_string\
                            (self.request.query_params['consumer_id']).id
                    if 'meter_id' in self.request.query_params:
                        self.request.query_params['meter_id'] = get_meter_by_id_string\
                            (self.request.query_params['meter_id']).id
                    self.request.query_params._mutable = False
                    queryset = ConsumerServiceContractDetail.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException
