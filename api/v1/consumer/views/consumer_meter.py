from rest_framework import generics, status
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.premises import get_premise_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.consumer.models.consumer_meter import ConsumerMeter
from v1.consumer.serializers.consumer_meter import ConsumerMeterListSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id_string


# API Header
# API end Point: api/v1/consumer/:id_string/meter/list
# API verb: GET
# Package: Basic
# Modules: Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Consumer meters
# Usage: API will fetch required data for Consumer meters
# Tables used: ConsumerMeter
# Author: Rohan
# Created on: 07/12/2020
class ConsumerMeterList(generics.ListAPIView):
    try:
        serializer_class = ConsumerMeterListSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerMeter.objects.filter(utility=utility, is_active=True)
                    if "premise_id" in self.request.query_params:
                        premise = get_premise_by_id_string(self.request.query_params['premise_id'])
                        queryset = queryset.filter(premise_id=premise.id)
                    if "service_contract_id" in self.request.query_params:
                        contract = get_utility_service_contract_master_by_id_string(self.request.query_params['service_contract_id'])
                        queryset = queryset.filter(service_contract_id=contract.id)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer meters not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Consumer')
