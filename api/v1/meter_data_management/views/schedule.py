__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from master.models import get_user_by_id_string
from v1.commonapp.views.logger import logger
from api.constants import CONSUMER_OPS, EDIT, METER_DATA, VIEW
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, SCHEDULE_NOT_FOUND
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.meter_data_management.serializers.schedule import ScheduleViewSerializer, ScheduleSerializer
from v1.meter_data_management.models.schedule import Schedule as ScheduleTbl, get_schedule_by_id_string


# API Header
# API end Point: api/v1/meter-data/schedule/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: schedule list
# Usage: API will fetch required data for schedule list against filter and search
# Tables used: Schedule
# Author: Akshay
# Created on: 06/01/2021

class ScheduleList(generics.ListAPIView):
    try:
        serializer_class = ScheduleViewSerializer
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
                    queryset = ScheduleTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException


# API Header
# API end Point: api/v1/schedule
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create schedule object
# Usage: API will create schedule object based on valid data
# Tables used: Schedule
# Author: Akshay
# Created on: 08/01/2021

class Schedule(GenericAPIView):
    @is_token_validate
    @role_required(CONSUMER_OPS, METER_DATA, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            print(request.data)
            schedule_serializer = ScheduleSerializer(data=request.data)
            if schedule_serializer.is_valid():
                print(schedule_serializer.validated_data)
                schedule_obj = schedule_serializer.create(schedule_serializer.validated_data, user)
                schedule_view_serializer = ScheduleViewSerializer(instance=schedule_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: schedule_view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: schedule_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/schedule/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View schedule object
# Usage: API will fetch and edit required data for schedule using id_string
# Tables used: Schedule
# Author: Akshay
# Created on: 08/01/2021

class ScheduleDetail(GenericAPIView):
    @is_token_validate
    @role_required(CONSUMER_OPS, METER_DATA, VIEW)
    def get(self, request, id_string):
        try:
            schedule_obj = get_schedule_by_id_string(id_string)
            if schedule_obj:
                serializer = ScheduleViewSerializer(instance=schedule_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: SCHEDULE_NOT_FOUND,
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
            schedule_obj = get_schedule_by_id_string(id_string)
            if schedule_obj:
                schedule_serializer = ScheduleSerializer(data=request.data)
                if schedule_serializer.is_valid():
                    schedule_obj = schedule_serializer.update(schedule_obj, schedule_serializer.validated_data, user)
                    schedule_view_serializer = ScheduleViewSerializer(instance=schedule_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: schedule_view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: schedule_serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: SCHEDULE_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
