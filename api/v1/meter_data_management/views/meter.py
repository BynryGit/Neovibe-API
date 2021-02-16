__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.messages import STATE, ERROR, EXCEPTION, SUCCESS, RESULT, METER_NOT_FOUND
from api.constants import CONSUMER_OPS, EDIT, METER_DATA, VIEW
from master.models import get_user_by_id_string
from v1.commonapp.models.lifecycle import LifeCycle
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.serializers.lifecycle import LifeCycleListSerializer
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.userapp.decorators import is_token_validate, role_required
from v1.meter_data_management.models.meter import Meter as MeterTbl, get_meter_by_id_string
from v1.meter_data_management.serializers.meter import MeterViewSerializer, MeterSerializer


# API Header
# API end Point: api/v1/meter-data/meter/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter list
# Usage: API will fetch required data for meter list against filter and search
# Tables used: Meter
# Author: Akshay
# Created on: 13/02/2021

class MeterList(generics.ListAPIView):
    try:
        serializer_class = MeterViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string',)
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    queryset = MeterTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException


# API Header
# API end Point: api/v1/meter
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create meter object
# Usage: API will create meter object based on valid data
# Tables used: Meter
# Author: Akshay
# Created on: 13/02/2021

class Meter(GenericAPIView):
    @is_token_validate
    @role_required(CONSUMER_OPS, METER_DATA, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
        except Exception as ex:
            print('exxx',ex)
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/meter/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View Edit Meter object
# Usage: API will fetch and edit required data for meter using id_string
# Tables used: Meter
# Author: Akshay
# Created on: 13/02/2021

class MeterDetail(GenericAPIView):
    @is_token_validate
    @role_required(CONSUMER_OPS, METER_DATA, VIEW)
    def get(self, request, id_string):
        try:
            meter_obj = get_meter_by_id_string(id_string)
            if meter_obj:
                serializer = MeterViewSerializer(instance=meter_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: METER_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(CONSUMER_OPS, METER_DATA, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            meter_obj = get_meter_by_id_string(id_string)
            if meter_obj:
                meter_serializer = MeterSerializer(data=request.data)
                if meter_serializer.is_valid():
                    meter_obj = meter_serializer.update(meter_obj, meter_serializer.validated_data, user)
                    meter_view_serializer = MeterViewSerializer(instance=meter_obj,
                                                                      context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: meter_view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: meter_serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: METER_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/meter/life-cycle/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter life cycle list
# Usage: API will fetch required data for meter life cycle list against filter and search
# Tables used: LifeCycle
# Author: Akshay
# Created on: 16/02/2021

class MeterLifeCycleList(generics.ListAPIView):
    try:
        serializer_class = LifeCycleListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'object_id')
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',)  # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1, 1, 1, user_obj):
                    self.request.query_params._mutable = True
                    module = get_module_by_key("CONSUMER_OPS")
                    sub_module = get_sub_module_by_key("METER_DATA")
                    if 'object_id' in self.request.query_params:
                        self.request.query_params['object_id'] = get_meter_by_id_string(self.request.query_params['object_id']).id
                    self.request.query_params._mutable = False
                    queryset = LifeCycle.objects.filter(module_id=module, sub_module_id=sub_module, is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException
