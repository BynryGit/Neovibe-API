__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from master.models import User as UserTbl, get_user_by_id_string
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.serializers.consumer import ConsumerViewSerializer
from v1.userapp.serializers.user import UserViewSerializer


# API Header
# API end Point: api/v1/meter-data/meterreader/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter reader list
# Usage: API will fetch required data for meter reader list against filter and search
# Tables used: User
# Author: Akshay
# Created on: 15/06/2020


class MeterReaderList(generics.ListAPIView):
    try:
        serializer_class = UserViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('email', 'tenant__id_string',)
        ordering_fields = ('email', 'tenant__id_string',)
        ordering = ('email',) # always give by default alphabetical order
        search_fields = ('email', 'tenant__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = UserTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/meterreader/id_string
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View meter reader object
# Usage: API will fetch required data for meter reader using id_string
# Tables used: User
# Author: Akshay
# Created on: 15/06/2020

class MeterReaderDetail(GenericAPIView):
    serializer_class = ConsumerViewSerializer

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

                    meter_reader_obj = get_user_by_id_string(id_string)
                    if meter_reader_obj:
                        serializer = UserViewSerializer(instance=meter_reader_obj, context={'request': request})
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
