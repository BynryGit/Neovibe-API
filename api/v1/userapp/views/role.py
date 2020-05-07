import traceback

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.messages import *
from api.settings import DISPLAY_DATE_FORMAT
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.department import get_department_by_tenant_id_string, get_department_by_id
from v1.commonapp.models.form_factor import get_form_factor_by_tenant_id_string, get_form_factor_by_id
from v1.commonapp.models.module import get_module_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.userapp.models.privilege import get_privilege_by_id
from v1.userapp.models.role_privilege import get_role_privilege_by_role_id
from v1.userapp.models.role_sub_type import get_role_sub_type_by_tenant_id_string, get_role_sub_type_by_id
from v1.userapp.models.role_type import get_role_type_by_tenant_id_string, get_role_type_by_id
from v1.userapp.models.user_master import get_user_by_id_string
from v1.userapp.models.user_role import get_role_by_id_string
from v1.userapp.views.common_functions import get_filtered_roles, is_data_verified, add_basic_role_details, \
    save_privilege_details, save_edited_basic_role_details, save_edited_privilege_details


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

class RoleList(APIView):

    def get(self, request, format=None):
        try:
            # Initializing output list start
            role_list = []
            # Initializing output list end

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

                    # Code for filtering roles start
                    user = get_user_by_id_string(request.data['user'])
                    result, roles, total_pages, page_no, error = get_filtered_roles(user, request)
                    if not result:
                        return Response({
                            STATE: EXCEPTION,
                            ERROR: error
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    # Code for filtering roles end

                    # Code for lookups start
                    types = get_role_type_by_tenant_id_string(user.tenant.id_string)
                    sub_types = get_role_sub_type_by_tenant_id_string(user.tenant.id_string)
                    # statuses = get_registration_statuses_by_tenant_id_string(user.tenant.id_string)
                    form_factors = get_form_factor_by_tenant_id_string(user.tenant.id_string)
                    departments = get_department_by_tenant_id_string(user.tenant.id_string)
                    # Code for lookups end

                    # Code for sending role in response start
                    for role in roles:
                        role_list.append({
                            'registration_id_string': role.id_string,
                            'name': role.role,
                            'type': types.get(id=role.type).name,
                            'sub_type': sub_types.get(id=role.sub_type).name,
                            'status': '',
                            'form_factor': form_factors.get(id=role.form_factor_id).name,
                            'department': departments.get(id=role.department_id).name,
                            'created_on': role.created_date.strftime(DISPLAY_DATE_FORMAT),
                            'total_pages': total_pages,
                            'page_no': page_no
                        })
                    return Response({
                        STATE: SUCCESS,
                        DATA: role_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending role in response end

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
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/registration
# API verb: GET, POST, PUT
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View roles, Add roles, Edit roles
# Usage: View, Add, Edit role
# Tables used: 2.5.1. Users & Privileges - Role Master
# Author: Arpita
# Created on: 05/05/2020

class Roles(APIView):

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
                    type = get_role_type_by_id(role.type_id)
                    sub_type = get_role_sub_type_by_id(role.state_id)
                    form_factor = get_form_factor_by_id(role.city_id)
                    department = get_department_by_id(role.area_id)
                    role_privileges = get_role_privilege_by_role_id(role.id)

                    for role_privilege in role_privileges:
                        module = get_module_by_id(role_privilege.module_id)
                        sub_module = get_sub_module_by_id(role_privilege.sub_module_id)
                        privilege = get_privilege_by_id(role_privilege.privilege_id)
                        privilege_list.append({
                            'module': module.name,
                            'sub_module': sub_module.name,
                            'privilege' : privilege.name
                        })
                    # Code for lookups end

                    # Code for sending role in response start
                    data = {
                        'tenant_id_string': role.tenant.id_string,
                        'utility_id_string': role.utility.id_string,
                        'type_id_string': type.id_string,
                        'sub_type_id_string': sub_type.id_string,
                        'form_factor_id_string': form_factor.id_string,
                        'department_id_string': department.id_string,
                        'role_no': role.role_ID,
                        'role_name': role.role,
                        'form_factor': form_factor.name,
                        'department': department.name,
                        'created_on': role.created_date.strftime(DISPLAY_DATE_FORMAT),
                        'privilege_list': privilege_list,
                        'is_active': role.is_active,
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                    # Code for sending role in response end

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
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic role details start
                        user = get_user_by_id_string(request.data['user'])
                        role, result, error = add_basic_role_details(request, user)
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
                    if is_data_verified(request):
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


class PrivilegeDetail(APIView):

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
                    if is_data_verified(request):
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
                    if is_data_verified(request):
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
