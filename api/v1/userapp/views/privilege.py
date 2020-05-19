import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import OrderingFilter, SearchFilter

from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.privilege import get_all_privilege, get_privilege_by_id_string
from v1.userapp.serializers.privilege import PrivilegeListSerializer, PrivilegeViewSerializer


# API Header
# API end Point: api/v1/user/privilege/list
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
    filter_fields = ('tenant__id_string', 'utility__id_string')
    ordering_fields = ('name',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('name',)

    def get_queryset(self):
        queryset = get_all_privilege()
        return queryset


# API Header
# API end Point: api/v1/user/privilege
# API verb: GET, POST, PUT
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View roles, Add roles, Edit Privileges
# Usage: View, Add, Edit role
# Tables used: 2.5.1. Users & Privileges - Privilege
# Author: Arpita
# Created on: 19/05/2020

class Privilege(GenericAPIView):

    def get(self, request, id_string):
        try:
            privilege = get_privilege_by_id_string(id_string)
            if privilege:
                serializer = PrivilegeViewSerializer(instance=privilege, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def post(self, request, format=None):
    #     try:
    #         # Checking authentication start
    #         if is_token_valid(request.data['token']):
    #             # payload = get_payload(request.data['token'])
    #             # user = get_user(payload['id_string'])
    #             # Checking authentication end
    #
    #             # Checking authorization start
    #             # privilege = get_privilege_by_id(1)
    #             # sub_module = get_sub_module_by_id(1)
    #             if is_authorized():
    #                 # Checking authorization end
    #
    #                 # Request data verification start
    #                 if is_role_data_verified(request):
    #                     # Request data verification end
    #
    #                     # Save basic role details start
    #                     # user = get_user_by_id_string(request.data['user_id_string'])
    #                     user = get_user_by_id(3)
    #                     serializer = RoleSerializer(data=request.data)
    #                     if serializer.is_valid():
    #                         role_obj = serializer.create(serializer.validated_data, user)
    #                         view_serializer = RoleViewSerializer(instance=role_obj, context={'request': request})
    #                         return Response({
    #                             STATE: SUCCESS,
    #                             RESULTS: view_serializer.data,
    #                         }, status=status.HTTP_201_CREATED)
    #                     else:
    #                         return Response({
    #                             STATE: ERROR,
    #                             RESULTS: serializer.errors,
    #                         }, status=status.HTTP_400_BAD_REQUEST)
    #                     # Save basic role details start
    #                 else:
    #                     return Response({
    #                         STATE: ERROR,
    #                     }, status=status.HTTP_400_BAD_REQUEST)
    #             else:
    #                 return Response({
    #                     STATE: ERROR,
    #                 }, status=status.HTTP_403_FORBIDDEN)
    #         else:
    #             return Response({
    #                 STATE: ERROR,
    #             }, status=status.HTTP_401_UNAUTHORIZED)
    #     except Exception as e:
    #         logger().log(e, 'ERROR', user='test', name='test')
    #         return Response({
    #             STATE: EXCEPTION,
    #             ERROR: str(traceback.print_exc(e))
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # def put(self, request, id_string):
    #     try:
    #         # Checking authentication start
    #         if is_token_valid(request.data['token']):
    #             # payload = get_payload(request.data['token'])
    #             # user = get_user(payload['id_string'])
    #             # Checking authentication end
    #
    #             # Checking authorization start
    #             # privilege = get_privilege_by_id(1)
    #             # sub_module = get_sub_module_by_id(1)
    #             if is_authorized():
    #                 # Checking authorization end
    #
    #                 # Request data verification start
    #                 if is_role_data_verified(request):
    #                     # Request data verification end
    #
    #                     # Save basic details start
    #                     # user = get_user_by_id_string(request.data['user'])
    #                     user = get_user_by_id(3)
    #                     role_obj = get_role_by_id_string(id_string)
    #                     if role_obj:
    #                         serializer = RoleSerializer(data=request.data)
    #                         if serializer.is_valid():
    #                             role_obj = serializer.update(role_obj, serializer.validated_data, user)
    #                             view_serializer = RoleViewSerializer(instance=role_obj, context={'request': request})
    #                             return Response({
    #                                 STATE: SUCCESS,
    #                                 RESULTS: view_serializer.data,
    #                             }, status=status.HTTP_200_OK)
    #                         else:
    #                             return Response({
    #                                 STATE: ERROR,
    #                                 RESULTS: serializer.errors,
    #                             }, status=status.HTTP_400_BAD_REQUEST)
    #                     else:
    #                         return Response({
    #                             STATE: ERROR,
    #                         }, status=status.HTTP_404_NOT_FOUND)
    #                 else:
    #                     return Response({
    #                         STATE: ERROR,
    #                     }, status=status.HTTP_400_BAD_REQUEST)
    #             else:
    #                 return Response({
    #                     STATE: ERROR,
    #                 }, status=status.HTTP_403_FORBIDDEN)
    #         else:
    #             return Response({
    #                 STATE: ERROR,
    #
    #             }, status=status.HTTP_401_UNAUTHORIZED)
    #     except Exception as e:
    #         logger().log(e, 'ERROR', user='test', name='test')
    #         return Response({
    #             STATE: EXCEPTION,
    #             ERROR: str(traceback.print_exc(e))
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
