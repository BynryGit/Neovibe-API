import traceback

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.messages import STATE, DATA, SUCCESS, ERROR, EXCEPTION
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.department import get_all_departments

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