__author__ = "aki"

import traceback

from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from master.models import User
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_module import get_utility_module_by_id_string, \
    UtilityModule as UtilityModuleTbl
from v1.utility.serializers.utility_module import UtilityModuleViewSerializer, UtilityModuleSerializer


# API Header
# API end Point: api/v1/utility/id_string/module/list
# API verb: GET
# Package: Basic
# Modules: Utility
# Sub Module: Module
# Interaction: Get utility module list
# Usage: API will fetch required data for utility module list against single utility
# Tables used: 2.3 Utility Module
# Author: Akshay
# Created on: 12/05/2020


class UtilityModuleList(generics.ListAPIView):
    try:
        serializer_class = UtilityModuleViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('module_name', 'tenant__name', 'utility__name')
        ordering = ('module_name',)  # always give by default alphabetical order
        search_fields = ('module_name', 'tenant__name', 'utility__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = UtilityModuleTbl.objects.filter(utility__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/utility/module/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Utility
# Sub Module: Module
# Interaction: For edit and get single utility module
# Usage: API will edit and get utility module
# Tables used: 2.3 Utility Module
# Author: Akshay
# Created on: 13/05/2020

class UtilityModuleDetail(GenericAPIView):
    serializer_class = UtilityModuleSerializer

    def get(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['Authorization']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end

                    utility_module_obj = get_utility_module_by_id_string(id_string)
                    if utility_module_obj:
                        serializer = UtilityModuleViewSerializer(utility_module_obj, context={'request': request})
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
            if is_token_valid(request.headers['Authorization']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    utility_module_obj = get_utility_module_by_id_string(id_string)
                    if utility_module_obj:
                        serializer = UtilityModuleSerializer(data=request.data)
                        if serializer.is_valid():
                            utility_module_obj = serializer.update(utility_module_obj, serializer.validated_data, user)
                            serializer = UtilityModuleViewSerializer(utility_module_obj, context={'request': request})
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