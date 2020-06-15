__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DUPLICATE, DATA_ALREADY_EXISTS, RESULT
from master.models import User
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.meter_reading.models.schedule import Schedule as ScheduleTbl, get_schedule_by_id_string
from v1.meter_reading.serializers.meter_reading import MeterReadingViewSerializer, MeterReadingSerializer


# API Header
# API end Point: api/v1/meter-data/meterreading
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter reading list
# Usage: API will fetch required data for meter reading list against filter and search
# Tables used: 2.3.8.4 Meter Reading
# Author: Akshay
# Created on: 15/06/2020


class MeterReadingList(generics.ListAPIView):
    try:
        serializer_class = MeterReadingViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('consumer_no', 'utility__id_string',)
        ordering_fields = ('consumer_no', 'utility__id_string',)
        ordering = ('consumer_no', 'utility__id_string',) # always give by default alphabetical order
        search_fields = ('consumer_no', 'utility__id_string',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = ScheduleTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/meterreading
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create meter reading object
# Usage: API will create meter reading object based on valid data
# Tables used: 2.3.8.4 Meter Reading
# Author: Akshay
# Created on: 15/06/2020

class MeterReading(GenericAPIView):
    serializer_class = MeterReadingSerializer

    def post(self, request):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    serializer = MeterReadingSerializer(data=request.data)
                    if serializer.is_valid():
                        schedule_obj = serializer.create(serializer.validated_data, user)
                        if schedule_obj:
                            serializer = MeterReadingViewSerializer(instance=schedule_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULT: serializer.data,
                            }, status=status.HTTP_201_CREATED)
                        else:
                            return Response({
                                STATE: DUPLICATE,
                                RESULT: DATA_ALREADY_EXISTS,
                            }, status=status.HTTP_409_CONFLICT)
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULT: serializer.errors,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/meterreading/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View meter reading object
# Usage: API will fetch and edit required data for meter reading using id_string
# Tables used: 2.3.8.4 Meter Reading
# Author: Akshay
# Created on: 15/06/2020

class MeterReadingDetail(GenericAPIView):
    serializer_class = MeterReadingSerializer

    def get(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end

                    schedule_obj = get_schedule_by_id_string(id_string)
                    if schedule_obj:
                        serializer = MeterReadingViewSerializer(instance=schedule_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    schedule_obj = get_schedule_by_id_string(id_string)
                    if schedule_obj:
                        serializer = MeterReadingSerializer(data=request.data)
                        if serializer.is_valid():
                            schedule_obj = serializer.update(schedule_obj, serializer.validated_data, user)
                            serializer = MeterReadingViewSerializer(instance=schedule_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULT: serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULT: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)