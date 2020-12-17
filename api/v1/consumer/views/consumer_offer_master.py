from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_credit_rating import ConsumerCreditRating
from v1.consumer.models.consumer_offer_master import ConsumerOfferMaster
from v1.consumer.serializers.consumer_credit_rating import ConsumerCreditRatingListSerializer


# API Header
# API end Point: api/v1/consumer/:id_string/credit-rating/list
# API verb: GET
# Interaction: Consumer Credit rating list
# Usage: API will fetch all Consumer credit rating List
# Tables used: Consumer credit rating
# Author: Rohan
# Created on: 17-12-2020
from v1.consumer.serializers.consumer_offer_master import ConsumerOfferMasterListSerializer
from v1.utility.models.utility_master import get_utility_by_id_string


class ConsumerOfferMasterList(generics.ListAPIView):
    try:
        serializer_class = ConsumerOfferMasterListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('offer_name', 'tenant__id_string',)
        ordering_fields = ('offer_name', 'tenant',)
        ordering = ('offer_name',)  # always give by default alphabetical order
        search_fields = ('offer_name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerOfferMaster.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer offers not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer ops', sub_module='Consumer')
