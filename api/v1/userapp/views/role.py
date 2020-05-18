import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import OrderingFilter, SearchFilter

from api.messages import *
from api.settings import DISPLAY_DATE_FORMAT
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.department import get_department_by_id, get_department_by_id_string
from v1.commonapp.models.form_factor import get_form_factor_by_id, get_form_factor_by_id_string
from v1.commonapp.models.module import get_module_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.privilege import get_privilege_by_id
from v1.userapp.models.role_privilege import get_role_privilege_by_role_id
from v1.userapp.models.role_sub_type import get_role_sub_type_by_id, get_role_sub_type_by_id_string
from v1.userapp.models.role_type import get_role_type_by_id, get_role_type_by_id_string
from v1.userapp.models.user_master import get_user_by_id_string, get_user_by_id
from v1.userapp.models.role import get_role_by_id_string, get_role_by_tenant_id_string, \
    get_role_by_utility_id_string, get_all_role
from v1.userapp.serializers.role import RoleListSerializer, RoleViewSerializer, RoleSerializer
from v1.userapp.views.common_functions import add_basic_role_details, save_privilege_details, \
    save_edited_basic_role_details, save_edited_privilege_details, is_role_data_verified


# API Header
# API end Point: api/v1/roles
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View role list
# Usage: Used for role list. Gets all the records in pagination mode. It also have input params to filter/search and
# sort in addition to pagination.
# Tables used: 2.5.1. Users & Privileges - Role Master
# Author: Arpita
# Created on: 04/05/2020
# Updated on: 09/05/2020

class RoleList(generics.ListAPIView):
    serializer_class = RoleListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('tenant__id_string', 'utility__id_string')
    # filter_fields = ('tenant__id_string', 'utility__id_string', 'type_id_string', 'sub_type_id_string', 'form_factor_id_string', 'department_id_string')
    ordering_fields = ('name',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('name',)

    def get_queryset(self):

        queryset = get_all_role()
        return queryset


# API Header
# API end Point: api/v1/roles
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View role list
# Usage: Used for role list. Gets all the records in pagination mode. It also have input params to filter/search and
# sort in addition to pagination.
# Tables used: 2.5.1. Users & Privileges - Role Master
# Author: Arpita
# Created on: 13/05/2020


class GetRoleList(generics.ListAPIView):
    serializer_class = RoleListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        queryset = get_all_role()
        return queryset


# API Header
# API end Point: api/v1/user/role
# API verb: GET, POST, PUT
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View roles, Add roles, Edit roles
# Usage: View, Add, Edit role
# Tables used: 2.5.1. Users & Privileges - Role Master
# Author: Arpita
# Created on: 05/05/2020
# Updated on: 12/05/2020

class Role(GenericAPIView):

    def get(self, request, id_string):
        try:
            role = get_role_by_id_string(id_string)
            if role:
                serializer = RoleViewSerializer(instance=role, context={'request': request})
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

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_role_data_verified(request):
                        # Request data verification end

                        # Save basic role details start
                        # user = get_user_by_id_string(request.data['user_id_string'])
                        user = get_user_by_id(3)
                        serializer = RoleSerializer(data=request.data)
                        if serializer.is_valid():
                            role_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = RoleViewSerializer(instance=role_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
                            }, status=status.HTTP_201_CREATED)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                        # Save basic role details start
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

    def put(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_role_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        user = get_user_by_id_string(request.data['user'])
                        role, result, error = save_edited_basic_role_details(request, user)
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
                        # Save basic details start
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


# API Header
# API end Point: api/v1/role/privileges
# API verb: GET, POST, PUT
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View privilege details, Add privilege details, Edit privilege details
# Usage: View, Add, Edit privilege details
# Tables used: 2.5.1. Users & Privileges - Role Master, Role Privileges
# Author: Arpita
# Created on: 06/05/2020

class PrivilegeDetail(APIView):

    def get(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
            # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                # Checking authorization end

                    # Declare local variables start
                    privilege_list = []
                    # Declare local variables end

                    # Code for lookups start
                    role = get_role_by_id_string(request.data['role_id_string'])
                    role_privileges = get_role_privilege_by_role_id(role.id)

                    for role_privilege in role_privileges:
                        module = get_module_by_id(role_privilege.module_id)
                        sub_module = get_sub_module_by_id(role_privilege.sub_module_id)
                        privilege = get_privilege_by_id(role_privilege.privilege_id)
                        privilege_list.append({
                            'module': module.name,
                            'sub_module': sub_module.name,
                            'privilege': privilege.name
                        })
                    # Code for lookups end

                    # Code for sending privileges in response start
                    data = {
                        'tenant_id_string': role.tenant.id_string,
                        'utility_id_string': role.utility.id_string,
                        'role_id_string': role.id_string,
                        'privilege_list': privilege_list,
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                    # Code for sending privileges in response end

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
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_role_data_verified(request):
                        # Request data verification end

                        # Save privilege details start
                        user = get_user_by_id_string(request.data['user'])
                        role = get_role_by_id_string(request.data['role'])
                        role_privilege, result, error = save_privilege_details(request, user, role)
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_role_data_verified(request):
                        # Request data verification end

                        # Save privilege details start
                        user = get_user_by_id_string(request.data['user'])
                        role = get_role_by_id_string(request.data['role'])
                        role_privilege, result, error = save_edited_privilege_details(request, user, role)
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)