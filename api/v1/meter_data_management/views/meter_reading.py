__author__ = "aki"

import json
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
##from api.constants import CONSUMER_OPS, EDIT, METER_DATA, VIEW
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, METER_READING_NOT_FOUND, READING_NOT_PROVIDED
from master.models import get_user_by_id_string
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.meter_data_management.serializers.meter_reading import MeterReadingViewSerializer, MeterReadingSerializer
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl, \
    get_meter_reading_by_id_string


# API Header
# API end Point: api/v1/meter-data/meter-reading/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter reading list
# Usage: API will fetch required data for meter reading list against filter and search
# Tables used: Meter Reading
# Author: Akshay
# Created on: 27/02/2021


class MeterReadingList(generics.ListAPIView):
    try:
        serializer_class = MeterReadingViewSerializer
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
                    queryset = MeterReadingTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException


# API Header
# API end Point: api/v1/meter-data/meter-reading
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create meter reading object
# Usage: API will create meter reading object based on valid data
# Tables used: Meter Reading
# Author: Akshay
# Created on: 09/03/2021

class MeterReading(GenericAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, METER_DATA, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            dict = {}
            if len(request.data) > 0:
                dict['image_missing'] = []
                dict['created_meter_reading'] = []
                dict['create_meter_reading_error'] = []
                dict['serializer_error'] = []
                image_dict = {}
                for data in request.data:
                    meter_image = data.get("meter_image")
                    if meter_image:
                        meter_reading_serializer = MeterReadingSerializer(data=data)
                        if meter_reading_serializer.is_valid():
                            meter_reading_obj = meter_reading_serializer.create(meter_reading_serializer.validated_data,
                                                                                user)
                            if meter_reading_obj:
                                dict['created_meter_reading'].append(data.get('consumer_detail_id'))
                                image_dict[meter_reading_obj.id] = {}
                                image_dict[meter_reading_obj.id]['meter_image'] = json.dumps(meter_image)
                            else:
                                dict['create_meter_reading_error'].append(data.get('consumer_detail_id'))
                        else:
                            dict['serializer_error'].append(data.get('consumer_detail_id'))
                    else:
                        dict['image_missing'].append(data.get('consumer_detail_id'))
                return Response({
                    STATE: SUCCESS,
                    RESULT: dict,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: SUCCESS,
                    RESULT: READING_NOT_PROVIDED,
                }, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/meter-data/meter-reading/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View schedule object
# Usage: API will fetch and edit required data for meter reading using id_string
# Tables used: Schedule
# Author: Akshay
# Created on: 27/02/2021

class MeterReadingDetail(GenericAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, METER_DATA, VIEW)
    def get(self, request, id_string):
        try:
            meter_reading_obj = get_meter_reading_by_id_string(id_string)
            if meter_reading_obj:
                serializer = MeterReadingViewSerializer(instance=meter_reading_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: METER_READING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    #role_required(CONSUMER_OPS, METER_DATA, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            meter_reading_obj = get_meter_reading_by_id_string(id_string)
            if meter_reading_obj:
                meter_reading_serializer = MeterReadingSerializer(data=request.data)
                if meter_reading_serializer.is_valid():
                    meter_reading_obj = meter_reading_serializer.update(meter_reading_obj, meter_reading_serializer.validated_data, user)
                    meter_reading_view_serializer = MeterReadingViewSerializer(instance=meter_reading_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: meter_reading_view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: meter_reading_serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: METER_READING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
