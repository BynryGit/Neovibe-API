import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.smart360_API.commonapp.models.area import get_areas_by_tenant_id_string
from api.v1.smart360_API.commonapp.models.sub_area import get_sub_areas_by_tenant_id_string
from api.v1.smart360_API.registration.views.common_functions import get_filtered_registrations, is_data_verified, \
    save_basic_registration_details, save_payment_details
from api.v1.smart360_API.commonapp.common_functions import get_payload,get_user,is_authorized,is_token_valid
from api.v1.smart360_API.lookup.models.privilege import get_privilege_by_id
from api.v1.smart360_API.lookup.models.sub_module import get_sub_module_by_id
from api.v1.smart360_API.smart360_API.messages import STATE,SUCCESS,ERROR,EXCEPTION
from api.v1.smart360_API.smart360_API.settings import DISPLAY_DATE_FORMAT


# API Header
# API end Point: api/v1/registration/list
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Registration list
# Usage: API will fetch required data for Registration list
# Tables used: 2.4.2. Consumer - Registration
# Auther: Rohan
# Created on: 21/04/2020


class RegistrationListApiView(APIView):

    def get(self, request, format=None):
        try:
            # Initializing output list start
            registrations_list = []
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

                    # Code for filtering registrations start
                    registrations,total_pages,page_no = get_filtered_registrations(user, request)
                    # Code for filtering registrations end

                    # Code for lookups start
                    statuses = Status.objects.all()
                    areas = get_areas_by_tenant_id_string(user.tenant.id_string)
                    sub_areas = get_sub_areas_by_tenant_id_string(user.tenant.id_string)
                    # Code for lookups end

                    # Code for sending registrations in response start
                    for registration in registrations:
                        registrations_list.append({
                            'first_name' : registration.first_name,
                            'last_name': registration.last_name,
                            'registration_no' : registration.registration_no,
                            'status' : statuses.objects.get(id_string = registration.status_id).status_name,
                            'mobile_no' : registration.phone_mobile,
                            'area' : areas.objects.get(id_string = registration.area_id).area_name,
                            'sub_area' : sub_areas.objects.get(id_string = registration.sub_area_id).sub_area_name,
                            'raised_on' : registration.registration_date.strftime(DISPLAY_DATE_FORMAT),
                            'total_pages': total_pages,
                            'page_no' : page_no
                        })
                    return Response({
                        STATE: SUCCESS,
                        'data': registrations_list,
                    }, status=status.HTTP_200_OK)
                    # Code for sending registrations in response end

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



class AddRegistrationApiView(APIView):
    def post(self, request, format=None):
        try:
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

                    # Request data verification start
                    if is_data_verified(request,user):
                    # Request data verification end

                        # Save basic and payment details start
                        registration = save_basic_registration_details(request, user)
                        payment = save_payment_details(request, user, registration) # TODO: Remaining
                        # Save basic and payment details start
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


