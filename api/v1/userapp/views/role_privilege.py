import traceback
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics
from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.userapp.models.user_master import get_user_by_id
from v1.userapp.serializers.role_privilege import RolePrivilegeSerializer, RolePrivilegeViewSerializer
from v1.userapp.views.common_functions import is_role_privilege_data_verified


# API Header
# API end Point: api/v1/role/privileges
# API verb: POST
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View privilege details, Add privilege details, Edit privilege details
# Usage: View, Add, Edit privilege details
# Tables used: 2.5.1. Users & Privileges - Role Master, Role Privileges
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 19/05/2020


class RolePrivilege(GenericAPIView):

    # def get(self, request, format=None):
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
    #                 # Declare local variables start
    #                 privilege_list = []
    #                 # Declare local variables end
    #
    #                 # Code for lookups start
    #                 role = get_role_by_id_string(request.data['role_id_string'])
    #                 role_privileges = get_role_privilege_by_role_id(role.id)
    #
    #                 for role_privilege in role_privileges:
    #                     module = get_module_by_id(role_privilege.module_id)
    #                     sub_module = get_sub_module_by_id(role_privilege.sub_module_id)
    #                     privilege = get_privilege_by_id(role_privilege.privilege_id)
    #                     privilege_list.append({
    #                         'module': module.name,
    #                         'sub_module': sub_module.name,
    #                         'privilege': privilege.name
    #                     })
    #                 # Code for lookups end
    #
    #                 # Code for sending privileges in response start
    #                 data = {
    #                     'tenant_id_string': role.tenant.id_string,
    #                     'utility_id_string': role.utility.id_string,
    #                     'role_id_string': role.id_string,
    #                     'privilege_list': privilege_list,
    #                 }
    #                 return Response({
    #                     STATE: SUCCESS,
    #                     DATA: data,
    #                 }, status=status.HTTP_200_OK)
    #                 # Code for sending privileges in response end
    #
    #             else:
    #                 return Response({
    #                     STATE: ERROR,
    #                     DATA: '',
    #                 }, status=status.HTTP_403_FORBIDDEN)
    #         else:
    #             return Response({
    #                 STATE: ERROR,
    #                 DATA: '',
    #             }, status=status.HTTP_401_UNAUTHORIZED)
    #     except Exception as e:
    #         return Response({
    #             STATE: EXCEPTION,
    #             DATA: '',
    #             ERROR: str(traceback.print_exc(e))
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_role_privilege_data_verified(request):
                        # Request data verification end

                        # Save privilege details start
                        user = get_user_by_id(3)
                        serializer = RolePrivilegeSerializer(data=request.data)
                        if serializer.is_valid():
                            privilege_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = RolePrivilegeViewSerializer(instance=privilege_obj,
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
                        # Save privilege details start
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def put(self, request, format=None):
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
    #                     # Save privilege details start
    #                     user = get_user_by_id_string(request.data['user'])
    #                     role = get_role_by_id_string(request.data['role'])
    #                     role_privilege, result, error = save_edited_privilege_details(request, user, role)
    #                     if result:
    #                         data = {
    #                             "role_id_string": role.id_string
    #                         }
    #                         return Response({
    #                             STATE: SUCCESS,
    #                             DATA: data,
    #                         }, status=status.HTTP_200_OK)
    #                     else:
    #                         return Response({
    #                             STATE: EXCEPTION,
    #                             ERROR: error
    #                         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #                     # Save privilege details start
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
    #         return Response({
    #             STATE: EXCEPTION,
    #             ERROR: str(traceback.print_exc(e))
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
