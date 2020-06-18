import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.filters import OrderingFilter, SearchFilter

from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import utility_required, is_token_validate, role_required
from v1.userapp.models.role import get_role_by_id_string, get_all_role
from v1.userapp.serializers.role import RoleListSerializer, RoleSerializer, RoleDetailViewSerializer


# API Header
# API end Point: api/v1/role/list
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View role list
# Usage: Used for role list. Gets all the records in pagination mode. It also have input params to filter/search and
# sort in addition to pagination.
# Tables used: 2.5.1. Users & Privileges - Role
# Author: Arpita
# Created on: 04/05/2020
# Updated on: 09/05/2020

class RoleList(generics.ListAPIView):
    serializer_class = RoleListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('role', 'tenant__id_string', 'utility__id_string')
    ordering_fields = ('role',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('role',)

    # @is_token_validate
    # @role_required(ADMIN, USER, VIEW)
    def get_queryset(self):
        queryset = get_all_role()
        return queryset


# API Header
# API end Point: api/v1/role
# API verb: POST
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: Add roles
# Usage: Add Role
# Tables used: 2.5.1. Users & Privileges - Role
# Author: Arpita
# Created on: 05/05/2020
# Updated on: 12/05/2020

class Role(GenericAPIView):

    @is_token_validate
    @utility_required
    @role_required(ADMIN, USER, EDIT)
    def post(self, request, format=None):
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                user_id_string = get_user_from_token(request.headers['token'])
                user = get_user_by_id_string(user_id_string)
                role_obj = serializer.create(serializer.validated_data, user)
                view_serializer = RoleDetailViewSerializer(instance=role_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/role/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: Get roles, Put roles
# Usage: Get Role, Put roles
# Tables used: 2.5.1. Users & Privileges - Role
# Author: Arpita
# Created on: 05/05/2020
# Updated on: 12/05/2020

class RoleDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, id_string):
        try:
            role = get_role_by_id_string(id_string)
            if role:
                serializer = RoleDetailViewSerializer(instance=role, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    RESULTS: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @utility_required
    @role_required(ADMIN, USER, EDIT)
    def put(self, request, id_string):
        try:
            role_obj = get_role_by_id_string(id_string)
            if role_obj:
                serializer = RoleSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    user_id_string = get_user_from_token(request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    role_obj = serializer.update(role_obj, serializer.validated_data, user)
                    view_serializer = RoleDetailViewSerializer(instance=role_obj, context={'request': request})
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
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)
