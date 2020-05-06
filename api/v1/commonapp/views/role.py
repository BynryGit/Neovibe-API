import traceback

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.messages import STATE, SUCCESS, DATA, ERROR, EXCEPTION
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.department import get_all_departments
from v1.commonapp.models.form_factor import get_all_form_factors
from v1.commonapp.models.module import get_module_by_id
from v1.commonapp.models.sub_module import get_all_sub_modules
from v1.userapp.models.role_sub_type import get_sub_type_by_type_id
from v1.userapp.models.role_type import get_all_role_type, get_role_type_by_id_string


# API Header
# API end Point: api/v1/roletypes
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Role Type
# Usage: This will get the list of role types
# Tables used: Lookup - Role Type
# Author: Arpita
# Created on: 06/05/2020


class RoleType(APIView):

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
                    role_type_list = []
                    # Declare local variables end

                    # Code for lookups start
                    role_types = get_all_role_type()
                    # Code for lookups end

                    # Code for sending role types in response start
                    for role_type in role_types:
                        data = {
                            'tenant_id_string': role_type.tenant.id_string,
                            'utility_id_string': role_type.utility.id_string,
                            'role_type_id_string': role_type.id_string,
                            'role_type': role_type.name,
                        }
                        role_type_list.append(data)
                    return Response({
                        STATE: SUCCESS,
                        DATA: role_type_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending role types in response end

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


# API Header
# API end Point: api/v1/rolesubtypes
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Role Sub Type
# Usage: This will get the list of role sub types according to role type
# Tables used: Lookup - Role Sub Type
# Author: Arpita
# Created on: 06/05/2020

class RoleSubType(APIView):

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
                    role_sub_type_list = []
                    # Declare local variables end

                    # Code for lookups start
                    role_type = get_role_type_by_id_string(request.data['role_type_id_string'])
                    role_sub_types = get_sub_type_by_type_id(role_type.id)
                    # Code for lookups end

                    # Code for sending role sub types in response start
                    for role_sub_type in role_sub_types:
                        data = {
                            'tenant_id_string': role_sub_type.tenant.id_string,
                            'utility_id_string': role_sub_type.utility.id_string,
                            'role_type_id_string': role_type.id_string,
                            'role_sub_type_id_string': role_sub_type.id_string,
                            'role_sub_type': role_sub_type.name,
                        }
                        role_sub_type_list.append(data)
                    return Response({
                        STATE: SUCCESS,
                        DATA: role_sub_type_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending role sub types in response end

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


# API Header
# API end Point: api/v1/form_factors
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Form Factor
# Usage: This will get the list of form factors
# Tables used: Lookup - 2.12.18 Lookup - Form Factor
# Author: Arpita
# Created on: 06/05/2020


class FormFactor(APIView):

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
                    form_factor_list = []
                    # Declare local variables end

                    # Code for lookups start
                    form_factors = get_all_form_factors()
                    # Code for lookups end

                    # Code for sending form factor in response start
                    for form_factor in form_factors:
                        data = {
                            'tenant_id_string': form_factor.tenant.id_string,
                            'utility_id_string': form_factor.utility.id_string,
                            'form_factor_id_string': form_factor.id_string,
                            'form_factor': form_factor.name,
                        }
                        form_factor_list.append(data)
                    return Response({
                        STATE: SUCCESS,
                        DATA: form_factor_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending form factor in response end

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


# API Header
# API end Point: api/v1/departments
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Departments
# Usage: This will get the list of departments
# Tables used: Lookup - 2.12.16 Lookup - Department
# Author: Arpita
# Created on: 06/05/2020


class Department(APIView):

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
                    department_list = []
                    # Declare local variables end

                    # Code for lookups start
                    departments = get_all_departments()
                    # Code for lookups end

                    # Code for sending departments in response start
                    for department in departments:
                        data = {
                            'tenant_id_string': department.tenant.id_string,
                            'utility_id_string': department.utility.id_string,
                            'department_id_string': department.id_string,
                            'department': department.name,
                        }
                        department_list.append(data)
                    return Response({
                        STATE: SUCCESS,
                        DATA: department_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending departments in response end

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


# API Header
# API end Point: api/v1/submodules
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Sub Modules
# Usage: This will get the list of sub modules
# Tables used: 2.12.26 Lookup - Module, 2.12.3. Lookup - Sub Module
# Author: Arpita
# Created on: 06/05/2020


class SubModule(APIView):

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
                    sub_module_list = []
                    # Declare local variables end

                    # Code for lookups start
                    sub_modules = get_all_sub_modules()
                    # Code for lookups end

                    # Code for sending departments in response start
                    for sub_module in sub_modules:
                        module = get_module_by_id(sub_module.module_id)
                        data = {
                            'module_id_string': module.id_string,
                            'module_name': module.name,
                            'sub_module_id_string': sub_module.id_string,
                            'sub_module_name': sub_module.id_string,
                        }
                        sub_module_list.append(data)
                    return Response({
                        STATE: SUCCESS,
                        DATA: sub_module_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending departments in response end

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