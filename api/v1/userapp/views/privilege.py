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
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import is_token_validate, role_required
from v1.userapp.models.privilege import get_all_privilege, get_privilege_by_id_string
from v1.userapp.serializers.privilege import PrivilegeListSerializer, PrivilegeViewSerializer, PrivilegeSerializer


# API Header
# API end Point: api/v1/privilege/list
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View privilege list
# Usage: Used for role list. Gets all the records in pagination mode. It also have input params to filter/search and
# sort in addition to pagination.
# Tables used: 2.5.1. Users & Privileges - Privilege
# Author: Arpita
# Created on: 19/05/2020


class PrivilegeList(generics.ListAPIView):
    serializer_class = PrivilegeListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name', 'tenant__id_string', 'utility__id_string')
    ordering_fields = ('name',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('name',)

    # @is_token_validate
    # @role_required(ADMIN, USER, VIEW)
    def get_queryset(self):
        queryset = get_all_privilege()
        return queryset


# API Header
# API end Point: api/v1/privilege
# API verb: POST
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View roles, Add roles, Edit Privileges
# Usage: Add role
# Tables used: 2.5.1. Users & Privileges - Privilege
# Author: Arpita
# Created on: 19/05/2020

class Privilege(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def post(self, request, format=None):
        try:
            serializer = PrivilegeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                user_id_string = get_user_from_token(request.headers['token'])
                user = get_user_by_id_string(user_id_string)
                privilege_obj = serializer.create(serializer.validated_data, user)
                view_serializer = PrivilegeViewSerializer(instance=privilege_obj,
                                                          context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'Privileges')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/privilege/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View roles, Edit Privileges
# Usage: View, Edit role
# Tables used: 2.5.1. Users & Privileges - Privilege
# Author: Arpita
# Created on: 19/05/2020

class PrivilegeDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, id_string):
        try:
            privilege = get_privilege_by_id_string(id_string)
            if privilege:
                serializer = PrivilegeViewSerializer(instance=privilege, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    RESULTS: PRIVILEGE_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'Privileges')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def put(self, request, id_string):
        try:
            role_obj = get_privilege_by_id_string(id_string)
            if role_obj:
                serializer = PrivilegeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    user_id_string = get_user_from_token(request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    privilege_obj = serializer.update(role_obj, serializer.validated_data, user)
                    view_serializer = PrivilegeViewSerializer(instance=privilege_obj,
                                                              context={'request': request})
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
                    RESULTS: PRIVILEGE_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'Privileges')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)
