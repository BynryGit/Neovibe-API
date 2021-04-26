from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id_string
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token, is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.serializers.consumer_offer_detail import ConsumerOfferDetailSerializer, \
    ConsumerOfferDetailListSerializer
from v1.userapp.decorators import is_token_validate, role_required
from v1.consumer.models.consumer_offer_detail import ConsumerOfferDetail as ConsumerOfferModel
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token, check_user

# API Header
# API end Point: api/v1/consumer/:id_string/offer-detail
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Add consumer offer detail
# Usage: Add
# Tables used: Consumer offer detail
# Author: Rohan
# Created on: 25/01/2021


class ConsumerOfferDetail(GenericAPIView):

    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER_OPS_CONSUMER, EDIT)
    def post(self, request, id_string):
        try:
            # user_id_string = get_user_from_token(request.headers['Authorization'])
            # user = get_user_by_id_string(user_id_string)
            user = check_user(request.headers['Authorization'])
            consumer = get_consumer_by_id_string(id_string)
            serializer = ConsumerOfferDetailSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                consumer_offer_detail = serializer.create(serializer.validated_data, consumer, user)
                if request.data['consumer_service_contract_id_string']:
                    consumer_service_contract_detail_obj = get_consumer_service_contract_detail_by_id_string(request.data['consumer_service_contract_id_string'])
                    consumer_offer_detail.consumer_service_contract_detail_id = consumer_service_contract_detail_obj.id
                    consumer_offer_detail.save()

                view_serializer = ConsumerOfferDetailSerializer(instance=consumer_offer_detail, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


class ConsumerOfferDetailList(generics.ListAPIView):
    try:
        serializer_class = ConsumerOfferDetailListSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.request.query_params['utility_id_string'])
                    queryset = ConsumerOfferModel.objects.filter(utility=utility, is_active=True)
                    if "consumer_id" in self.request.query_params:
                        consumer = get_consumer_by_id_string(self.request.query_params['consumer_id'])
                        queryset = queryset.filter(consumer_id=consumer.id)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumers offer details not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer ops', sub_module='Consumer')