
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.consumer.models.offer_sub_type import OfferSubType as OfferSubTypeModel, get_offer_sub_type_by_id_string
from v1.consumer.serializers.offer_sub_type import OfferSubTypeListSerializer, \
    OfferSubTypeViewSerializer, OfferSubTypeSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.utility.models.utility_master import get_utility_by_id_string
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
from v1.commonapp.views.custom_filter_backend import CustomFilter


# API Header
# API end Point: api/v1/consumer/utility/:id_string/offer_subtype/list
# API verb: GET
# Interaction: Consumer offer Subtype list
# Usage: API will fetch all Consumer offer Subtype List
# Tables used: OfferSubType
# Author: Chinmay
# Created on: 2-2-2021
class OfferSubTypeList(generics.ListAPIView):
    try:
        serializer_class = OfferSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = OfferSubTypeModel.objects.filter(utility=utility, is_active=True)
                    queryset = CustomFilter.get_offer_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer offers sub type not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer ops', sub_module='Consumer')


# API Header
# API end Point: api/v1/consumer/offer_subtype
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Offer SubType post
# Usage: API will Post the offers Subtype
# Tables used: OfferSubType
# Author: Chinmay
# Created on: 2/2/2021
class OfferSubType(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = OfferSubTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                offer_subtype_obj = serializer.create(serializer.validated_data, user)
                view_serializer = OfferSubTypeViewSerializer(instance=offer_subtype_obj, context={'request': request})
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
# API end Point: api/v1/consumer/offer_subtype/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Consumer Offer SubType corresponding to the id
# Usage: API will fetch and update offer SubTypes for a given id
# Tables used: OfferSubType
# Author: Chinmay
# Created on: 2/2/2021


class OfferSubTypeDetail(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            offer_subtype = get_offer_sub_type_by_id_string(id_string)
            if offer_subtype:
                serializer = OfferSubTypeViewSerializer(instance=offer_subtype, context={'request': request})
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
            offer_subtype_obj = get_offer_sub_type_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = offer_subtype_obj.name
            if offer_subtype_obj:
                serializer = OfferSubTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    offer_subtype_obj = serializer.update(offer_subtype_obj, serializer.validated_data, user)
                    view_serializer = OfferSubTypeViewSerializer(instance=offer_subtype_obj,
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
