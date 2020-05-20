import traceback
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics
from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.commonapp.views.logger import logger
from v1.userapp.models.privilege import get_privilege_by_id
from v1.userapp.models.role import get_role_by_id_string
from v1.userapp.models.role_privilege import get_role_privilege_by_role_id
from v1.userapp.models.user_master import get_user_by_id
from v1.userapp.serializers.privilege import GetPrivilegeSerializer
from v1.userapp.serializers.role import GetRoleSerializer
from v1.userapp.serializers.role_privilege import RolePrivilegeSerializer, RolePrivilegeViewSerializer
from v1.userapp.views.common_functions import is_role_privilege_data_verified


# API Header
# API end Point: api/v1/role/privileges
# API verb: POST
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: Add role-privilege details
# Usage: Add privilege details
# Tables used: 2.5.1. Users & Privileges - Role Privileges
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 20/05/2020


class RolePrivilege(GenericAPIView):

    def post(self, request, format=None):
        try:
            if is_token_valid(request.data['token']):
                if is_authorized():
                    if is_role_privilege_data_verified(request):
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/role/:id_string/privileges
# API verb: POST
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View privilege details, Edit privilege details
# Usage: View, Edit privilege details
# Tables used: 2.5.1. Users & Privileges - Role, Role Privileges
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 20/05/2020


class RolePrivilegeDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    sub_modules = []
                    data = []
                    role = get_role_by_id_string(id_string)
                    if role:
                        roles = GetRoleSerializer(instance=role, context={'request': request})
                        data.append(roles.data)
                        role_privileges = get_role_privilege_by_role_id(role.id)
                        for role_privilege in role_privileges:
                            sub_module_obj = get_sub_module_by_id(role_privilege.sub_module_id)
                            sub_module = SubModuleSerializer(instance=sub_module_obj, context={'request': request})
                            sub_modules.append(sub_module.data)
                            privilege_obj = get_privilege_by_id(role_privilege.privilege_id)
                            privilege = GetPrivilegeSerializer(instance=privilege_obj, context={'request': request})
                            index = sub_modules.index(sub_module.data)
                            sub_modules[index]['privilege'] = privilege.data

                        data[0]['sub_module'] = sub_modules
                        return Response({
                            STATE: SUCCESS,
                            DATA: data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        STATE: ERROR,
                        DATA: '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                if is_authorized():
                    if is_role_privilege_data_verified(request):
                        user = get_user_by_id(3)
                        role = get_role_by_id_string(request.data['role'])
                        # role_privilege, result, error = save_edited_privilege_details(request, user, role)
                        result = ''
                        if result:
                            data = {
                                "role_id_string": role.id_string
                            }
                            return Response({
                                STATE: SUCCESS,
                                DATA: data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: error
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

