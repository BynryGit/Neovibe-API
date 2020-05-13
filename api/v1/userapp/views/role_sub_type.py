import traceback

from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.userapp.serializers.role_sub_type import RoleSubTypeListSerializer, RoleSubTypeViewSerializer
from api.messages import *
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.role_sub_type import get_role_sub_type_by_tenant_id_string, get_role_sub_type_by_id_string


# API Header
# API end Point: api/v1/role_subtype/list
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Role Sub Type
# Usage: This will get the list of role sub types according to role type
# Tables used: Lookup - Role Sub Type
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 12/05/2020



class RoleSubTypeList(generics.ListAPIView):
    serializer_class = RoleSubTypeListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = get_role_sub_type_by_tenant_id_string(1)
        utility_id_string = self.request.query_params.get('utility', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        return queryset


# API Header
# API end Point: api/v1/role_subtype
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Role Sub Type
# Usage: This will get the detail of role sub types according to role type
# Tables used: Lookup - Role Sub Type
# Author: Arpita
# Created on: 12/05/2020

class RoleSubType(GenericAPIView):

    def get(self, request, id_string):
        try:
            role_sub_type = get_role_sub_type_by_id_string(id_string)
            if role_sub_type:
                serializer = RoleSubTypeViewSerializer(instance=role_sub_type, context={'request': request})
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
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class RoleSubType(APIView):
#
#     def get(self, request, format=None):
#         try:
#             # Checking authentication start
#             if is_token_valid(request.data['token']):
#                 # payload = get_payload(request.data['token'])
#                 # user = get_user(payload['id_string'])
#                 # Checking authentication end
#
#                 # Checking authorization start
#                 # privilege = get_privilege_by_id(1)
#                 # sub_module = get_sub_module_by_id(1)
#                 if is_authorized():
#                     # Checking authorization end
#
#                     # Declare local variables start
#                     role_sub_type_list = []
#                     # Declare local variables end
#
#                     # Code for lookups start
#                     role_type = get_role_type_by_id_string(request.data['role_type_id_string'])
#                     role_sub_types = get_sub_type_by_type_id(role_type.id)
#                     # Code for lookups end
#
#                     # Code for sending role sub types in response start
#                     for role_sub_type in role_sub_types:
#                         role_sub_type_list.append({
#                             'role_sub_type_id_string': role_sub_type.id_string,
#                             'role_sub_type': role_sub_type.name,
#                         })
#                     data = {'role_type_id_string': role_type.id_string, 'role_type_id': role_type.id,
#                             'role_sub_types': role_sub_type_list}
#                     return Response({
#                         STATE: SUCCESS,
#                         DATA: data,
#                     }, status=status.HTTP_200_OK)
#                     # Code for sending role sub types in response end
#
#                 else:
#                     return Response({
#                         STATE: ERROR,
#                         DATA: '',
#                     }, status=status.HTTP_403_FORBIDDEN)
#             else:
#                 return Response({
#                     STATE: ERROR,
#                     DATA: '',
#                 }, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             return Response({
#                 STATE: EXCEPTION,
#                 DATA: '',
#                 ERROR: str(traceback.print_exc(e))
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
