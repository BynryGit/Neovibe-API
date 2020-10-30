__author__ = "priyanka"

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
from v1.userapp.models.role_type import RoleType as RoleTypeTbl
from v1.userapp.serializers.role_type import GetRoleTypeSerializer


# API Header
# API end Point: api/v1/role/type
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: Role
# Interaction: Get Role Type list
# Usage: API will fetch required data for Role Type list 
# Tables used: Role Type
# Author: Priyanka
# Created on: 20/10/2020



class RoleTypeList(generics.ListAPIView):
    try:
        serializer_class = GetRoleTypeSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('name', 'tenant__name', 'utility__name')
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name', 'utility__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = RoleTypeTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException

# API Header
# API end Point: api/v1/role/type
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: Role
# Interaction: Get Role Type list
# Usage: API will fetch required data for Role Type list 
# Tables used: Role Type
# Author: Priyanka
# Created on: 20/10/2020



class RoleTypeListByUtility(generics.ListAPIView):
    try:
        serializer_class = GetRoleTypeSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('name', 'tenant__name', 'utility__name')
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name', 'utility__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = RoleTypeTbl.objects.filter(utility__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException