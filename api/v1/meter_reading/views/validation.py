__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from master.models import User
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.meter_reading.models.validation import Validation as ValidationTbl, get_validation_by_id_string
from v1.meter_reading.serializers.validation import ValidationViewSerializer, ValidationSerializer


# API Header
# API end Point: api/v1/validation/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: validation list
# Usage: API will fetch required data for validation list against filter and search
# Tables used: 2.3.8.7 Validation
# Author: Akshay
# Created on: 17/06/2020

class ValidationList(generics.ListAPIView):
    try:
        serializer_class = ValidationViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('consumer_no', 'utility__id_string',)
        ordering_fields = ('consumer_no', 'utility__id_string',)
        ordering = ('consumer_no',) # always give by default alphabetical order
        search_fields = ('consumer_no', 'utility__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = ValidationTbl.objects.filter(validator_id=1, is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/validation/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View adn Edit validation object
# Usage: API will fetch and edit required data for validation using id_string
# Tables used: 2.3.8.7 Validation
# Author: Akshay
# Created on: 17/06/2020

class ValidationDetail(GenericAPIView):
    serializer_class = ValidationSerializer

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

                    validation_obj = get_validation_by_id_string(id_string)
                    if validation_obj:
                        serializer = ValidationViewSerializer(instance=validation_obj, context={'request': request})
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

                    validation_obj = get_validation_by_id_string(id_string)
                    if validation_obj:
                        serializer = ValidationSerializer(data=request.data)
                        if serializer.is_valid():
                            validation_obj = serializer.update(validation_obj, serializer.validated_data, user)
                            serializer = ValidationViewSerializer(instance=validation_obj, context={'request': request})
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