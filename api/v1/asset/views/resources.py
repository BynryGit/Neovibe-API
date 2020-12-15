__author__ = "Priyanka"

import traceback
import logging
from datetime import datetime
from django.db import transaction
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.common_functions import is_token_valid, get_payload, is_authorized
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS,DUPLICATE,DATA_ALREADY_EXISTS
from v1.userapp.serializers.user import UserListSerializer,UserViewSerializer,UserSerializer

# API Header
# API end Point: api/v1/asset/resource
# API verb: GET
# Package: Basic
# Modules: O&M
# Sub Module:
# Interaction: resource List
# Usage: API will fetch required data for resource list
# Tables used:  Asset Master
# Author: Priyanka Kachare
# Created on: 21/05/2020

# Api for getting Asset  list

class ResourceList(generics.ListAPIView):
    try:
        serializer_class = UserListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('username', 'tenant__id_string','phone_mobile')
        ordering_fields = ('username','phone_mobile')
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('username','phone_mobile')

        def get_queryset(self):
            if is_token_valid(0):
                if is_authorized():
                    queryset = User.objects.filter(tenant=1,utility=1)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/asset/resource
# API verb: GET, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View users, Edit users
# Usage: View, Edit User
# Tables used: 2.5.3. Users & Privileges - User Details
# Author: Priyanka
# Created on: 27/05/2020


class ResourceDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    user = get_user_by_id_string(id_string)
                    if user:
                        serializer = UserViewSerializer(instance=user, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            RESULTS: '',
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    user = get_user_by_id_string(id_string)
                    # success, user = is_token_valid(self.request.headers['token'])
                    user_obj = get_user_by_id_string(id_string)
                    if user_obj:
                        serializer = UserSerializer(data=request.data)
                        if serializer.is_valid():
                            user_obj = serializer.update(user_obj, serializer.validated_data, user)
                            view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
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
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
