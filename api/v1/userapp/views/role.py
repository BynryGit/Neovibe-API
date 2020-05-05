import traceback

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.messages import *
from api.settings import DISPLAY_DATE_FORMAT
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.department import Department, get_department_by_tenant_id_string
from v1.commonapp.models.form_factor import FormFactor, get_form_factor_by_tenant_id_string
from v1.userapp.models.role_sub_type import RoleSubType, get_role_sub_type_by_tenant_id_string
from v1.userapp.models.role_type import RoleType, get_role_type_by_tenant_id_string
from v1.userapp.models.user_master import UserDetail
from v1.userapp.views.common_functions import get_filtered_roles


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
                    user = UserDetail.objects.get(id_string=request.data['user'])
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

                    # Code for sending registrations in response start
                    for role in roles:
                        role_list.append({
                            'registration_id_string': role.id_string,
                            'name': role.role,
                            'type': types.get(id=role.type).name,
                            'sub_type': sub_types.get(id=role.sub_type).name,
                            'status': '',
                            'form_factor': form_factors.get(id=role.form_factor_id).name,
                            'department': departments.get(id=role.department_id).name,
                            'created_on': role.created_date,
                            'total_pages': total_pages,
                            'page_no': page_no
                        })
                    return Response({
                        STATE: SUCCESS,
                        DATA: role_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending registrations in response end

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