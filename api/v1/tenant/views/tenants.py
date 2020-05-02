import traceback

from pyatspi import state
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.smart360_API.commonapp.models.state import get_state_by_id_string
from api.v1.smart360_API.smart360_API.messages import STATE, SUCCESS, ERROR, EXCEPTION, DATA
from api.v1.smart360_API.smart360_API.settings import DISPLAY_DATE_FORMAT
from api.v1.smart360_API.commonapp.common_functions import get_payload, get_user, is_authorized, is_token_valid
from api.v1.smart360_API.tenant.models.tenant_master import get_tenant
from api.v1.smart360_API.userapp.models.privilege import get_privilege_by_id
from api.v1.smart360_API.commonapp.models.sub_module import get_sub_module_by_id
from api.v1.smart360_API.commonapp.models.country import get_country_by_id_string, get_country_by_id
from api.v1.smart360_API.commonapp.models.city import get_city_by_id_string, get_city_by_id
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.models.area import get_areas_by_tenant_id_string, get_area_by_id
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id


# API Header
# API end Point: api/v1/tenant/list
# API verb: GET
# Package: Basic
# Modules: Tenant
# Sub Module:
# Interaction: Tenant List
# Usage: API will fetch required data for Tenant list
# Tables used: 1.1 Tenant
# Author: Gauri
# Created on: 28/04/2020

class TenantApiView(APIView):

    def get(self, request, format=None):
        try:
            # Initializing output list start
            tenant_list = []
            # Initializing output list end

            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end

                    # Code for filtering Tenant start
                    tenants, total_pages, page_no = get_tenant(user, request)
                    # Code for filtering tenant end

                    # Code for lookups start
                    statuses = Status.objects.all()
                    countries = get_country_by_id_string(user.tenant.id_string)
                    state = get_state_by_id_string(user.tenant.id_string)
                    # Code for lookups end

                    # Code for sending tenant in response start
                    for tenant in tenants:
                        tenant_list.append({
                            'first_name': tenant.first_name,
                            'phone_no': tenant.phone_no,
                            'email_id': tenant.email_id,
                            'status': statuses.objects.get(id_string=tenant.status_id).status_name,
                            # 'area': areas.objects.get(id_string=registration.area_id).area_name,
                            'country_id': countries.objects.get(id_string=tenant.country_id).country_name,
                            'state_id': state.objects.get(id_string=tenant.state_id).state_name,
                            'total_pages': total_pages,
                            'page_no': page_no
                        })
                    return Response({
                        STATE: SUCCESS,
                        'data': tenant_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending tenant in response end

                else:
                    return Response({
                        STATE: ERROR,
                        'data': '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    'data': '',
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # API Header
        # API end Point: api/v1/tenant/
        # API verb: GET, POST, PUT
        # Package: Basic
        # Modules: All
        # Sub Module: Tenant
        # Interaction: View Tenant, Add Tenant, Edit Tenants
        # Usage: View, Add, Edit Tenants
        # Tables used: 1.1 Tenant
        # Auther: Gauri
        # Created on: 29/04/2020

    class TenantApiView(APIView):


def get(self, request, format=None):
    try:
        # Checking authentication start
        if is_token_valid(request.data['token']):
            payload = get_payload(request.data['token'])
            user = get_user(payload['id_string'])
            # Checking authentication end

            # Checking authorization start
            privilege = get_privilege_by_id(1)
            if is_authorized(user, privilege):
                # Checking authorization end

                # Code for lookups start
                tenant = get_tenant(request.data['id_string'])
                country = get_country_by_id(tenant.country_id)

                # Code for sending registrations in response start
                data = {
                    'tenant_id_string': tenant.id_string,
                    'first_name': tenant.name,
                    'email_id': tenant.email_id,
                    'mobile_no': tenant.phone_mobile,
                    'country_id_string': country.id_string,
                    'state_id_string': state.id_string,
                    'city_id_string': city.id_string,
                    'area_id_string': area.id_string,
                    'is_active': tenant.is_active,
                }
                return Response({
                    STATE: SUCCESS,
                    DATA: data,
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
            DATA: '',
            ERROR: str(traceback.print_exc(e))
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
