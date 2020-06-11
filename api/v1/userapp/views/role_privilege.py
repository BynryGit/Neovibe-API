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
from v1.userapp.models.role_privilege import get_role_privilege_by_role_id, get_record_by_values, \
    get_record_values_by_id
from v1.userapp.serializers.privilege import GetPrivilegeSerializer
from v1.userapp.serializers.role import GetRoleSerializer
from v1.userapp.serializers.role_privilege import RolePrivilegeSerializer, RolePrivilegeViewSerializer
from v1.userapp.views.common_functions import set_role_privilege_validated_data


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
            response, user = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user):
                    data = []
                    module_list = request.data['module_id']
                    for module in module_list:
                        validate_data = {}
                        sub_module_list = module['sub_module_id']
                        for sub_module in sub_module_list:
                            validate_data['role_id'] = request.data['role_id']
                            validate_data['module_id'] = module['module_id']
                            validate_data['sub_module_id'] = sub_module['sub_module_id']
                            validate_data['privilege_id'] = sub_module['privilege_id']
                            validate_data['is_active'] = sub_module['is_active']
                            serializer = RolePrivilegeSerializer(data=validate_data)
                            if serializer.is_valid(raise_exception=False):
                                privilege_obj = serializer.create(serializer.validated_data, user)
                                view_serializer = RolePrivilegeViewSerializer(instance=privilege_obj,
                                                                          context={'request': request})
                                data.append(view_serializer.data)
                            else:
                                return Response({
                                    STATE: ERROR,
                                    RESULTS: serializer.errors,
                                }, status=status.HTTP_400_BAD_REQUEST)
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: data,
                    }, status=status.HTTP_201_CREATED)
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
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


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
            response, user_obj = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
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
                            RESULTS: data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            RESULTS: '',
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: '',
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
            # Checking authentication start
            response, user = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user):
                    data = []
                    role = get_role_by_id_string(id_string)
                    if role:
                        module_list = request.data['module_id']
                        for module in module_list:
                            validate_data = {}
                            sub_module_list = module['sub_module_id']
                            for sub_module in sub_module_list:
                                validate_data['role_id'] = str(id_string)
                                validate_data['module_id'] = module['module_id']
                                validate_data['sub_module_id'] = sub_module['sub_module_id']
                                validate_data['privilege_id'] = sub_module['privilege_id']
                                validate_data['is_active'] = sub_module['is_active']
                                validated_data = set_role_privilege_validated_data(validate_data)
                                serializer = RolePrivilegeSerializer(data=validated_data)
                                if serializer.is_valid(raise_exception=False):
                                    role_privilege = get_record_values_by_id(role.id, validate_data['module_id'],
                                                                          validate_data['sub_module_id'],
                                                                          validate_data['privilege_id'])

                                    if role_privilege:
                                        role_privilege_obj = serializer.update(role_privilege, serializer.validated_data, user)
                                    else:
                                        role_privilege_obj = serializer.create(serializer.validated_data, user)
                                    view_serializer = RolePrivilegeViewSerializer(instance=role_privilege_obj,
                                                                                  context={'request': request})
                                    data.append(view_serializer.data)
                                else:
                                    return Response({
                                        STATE: ERROR,
                                        RESULTS: serializer.errors,
                                    }, status=status.HTTP_400_BAD_REQUEST)
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: data,
                            }, status=status.HTTP_200_OK)
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
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


