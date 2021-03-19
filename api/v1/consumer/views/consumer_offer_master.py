from v1.utility.models.utility_product import UtilityProduct
from v1.utility.models.utility_service_contract_master import UtilityServiceContractMaster
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id_string
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.consumer.models.consumer_credit_rating import ConsumerCreditRating
from v1.consumer.models.consumer_offer_master import ConsumerOfferMaster as ConsumerOfferMasterModel, get_consumer_offer_master_by_id_string
from v1.consumer.serializers.consumer_credit_rating import ConsumerCreditRatingListSerializer
from v1.consumer.serializers.consumer_offer_master import ConsumerOfferMasterListSerializer, \
    ConsumerOfferMasterViewSerializer, ConsumerOfferMasterSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.utility.models.utility_master import UtilityMaster, get_utility_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/consumer/:id_string/credit-rating/list
# API verb: GET
# Interaction: Consumer Credit rating list
# Usage: API will fetch all Consumer credit rating List
# Tables used: Consumer credit rating
# Author: Rohan
# Created on: 17-12-2020
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
                    if "consumer_service_contract_id_string" in self.request.query_params:
                        consumer_contract_detail_obj = get_consumer_service_contract_detail_by_id_string(self.request.query_params["consumer_service_contract_id_string"])
                        utility_product_obj_id = UtilityServiceContractMaster.objects.get(id=consumer_contract_detail_obj.service_contract_id).utility_product_id
                        utility_product_obj = UtilityProduct.objects.get(id=utility_product_obj_id)
                        queryset = ConsumerOfferMasterModel.objects.filter(utility=utility, is_active=True, utility_product_id=utility_product_obj.id)
                    else:
                        queryset = ConsumerOfferMasterModel.objects.filter(utility=utility, is_active=True)
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


# API Header
# API end Point: api/v1/consumer/offer
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Offer post
# Usage: API will Post the offers
# Tables used: ConsumerOfferMaster
# Author: Chinmay
# Created on: 2/2/2021
class ConsumerOfferMaster(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = ConsumerOfferMasterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                offer_obj = serializer.create(serializer.validated_data, user)
                view_serializer = ConsumerOfferMasterViewSerializer(instance=offer_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/offer/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Consumer Offer corresponding to the id
# Usage: API will fetch and update Consumer Offers for a given id
# Tables used: ConsumerOfferMaster
# Author: Chinmay
# Created on: 2/2/2021


class ConsumerOfferMasterDetail(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            consumer_offer_master = get_consumer_offer_master_by_id_string(id_string)
            if consumer_offer_master:
                serializer = ConsumerOfferMasterViewSerializer(instance=consumer_offer_master, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            consumer_offer_master_obj = get_consumer_offer_master_by_id_string(id_string)
            if "offer_name" not in request.data:
                request.data['offer_name'] = consumer_offer_master_obj.offer_name
            if consumer_offer_master_obj:
                serializer = ConsumerOfferMasterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    consumer_offer_master_obj = serializer.update(consumer_offer_master_obj, serializer.validated_data, user)
                    view_serializer = ConsumerOfferMasterViewSerializer(instance=consumer_offer_master_obj,
                                                                        context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)
