import traceback

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.messages import STATE, DATA, SUCCESS, ERROR, EXCEPTION
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.form_factor import get_all_form_factors

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