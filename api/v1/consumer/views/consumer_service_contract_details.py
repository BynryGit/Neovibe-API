from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter

from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.models.consumer_service_contract_details import ConsumerServiceContractDetail
from v1.consumer.serializers.consumer_service_contract_details import ConsumerServiceContractDetailViewSerializer


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
