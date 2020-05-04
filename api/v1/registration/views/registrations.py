import traceback

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.settings import DISPLAY_DATE_FORMAT
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.models.area import get_areas_by_tenant_id_string, get_area_by_id
from v1.userapp.models.user_master import SystemUser
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.consumer_category import get_consumer_category_by_id
from v1.commonapp.models.consumer_sub_category import get_consumer_sub_category_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.sub_area import get_sub_areas_by_tenant_id_string, get_sub_area_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.source_type import get_source_type_by_id
from v1.registration.models.registration_status import get_registration_status_by_id_string, \
    get_registration_statuses_by_tenant_id_string, RegistrationStatus
from v1.registration.models.registration_type import get_registration_type_by_id
from v1.registration.models.registrations import get_registration_by_id_string
from v1.registration.views.common_functions import get_filtered_registrations, is_data_verified, \
    save_basic_registration_details, save_payment_details
from v1.userapp.models.privilege import get_privilege_by_id
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA


# API Header
# API end Point: api/v1/registration/list api/v1/registrations
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Registration list
# Usage: API will fetch required data for Registration list
# Tables used: 2.4.2. Consumer - Registration
# Author: Rohan
# Created on: 21/04/2020
class RegistrationListApiView(APIView):

    def get(self, request, format=None):
        try:
            # Initializing output list start
            registrations_list = []
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

                    # Code for filtering registrations start
                    user = SystemUser.objects.get(id=3)
                    registrations, total_pages, page_no, result, error = get_filtered_registrations(user, request)
                    if result == False:
                        return Response({
                            STATE: EXCEPTION,
                            ERROR: error
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    # Code for filtering registrations end

                    # Code for lookups start
                    statuses = get_registration_statuses_by_tenant_id_string(user.tenant.id_string)
                    areas = get_areas_by_tenant_id_string(user.tenant.id_string)
                    sub_areas = get_sub_areas_by_tenant_id_string(user.tenant.id_string)
                    # Code for lookups end

                    # Code for sending registrations in response start
                    for registration in registrations:
                        registrations_list.append({
                            'registration_id_string': registration.id_string,
                            'first_name': registration.first_name,
                            'last_name': registration.last_name,
                            'registration_no': registration.registration_no,
                            'status': statuses.get(id=registration.status_id).name,
                            'mobile_no': registration.phone_mobile,
                            'area': areas.get(id=registration.area_id).name,
                            'sub_area': sub_areas.get(id=registration.sub_area_id).name,
                            'raised_on': registration.registration_date.strftime(DISPLAY_DATE_FORMAT),
                            'total_pages': total_pages,
                            'page_no': page_no
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


# API Header
# API end Point: api/v1/registration
# API verb: GET, POST, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: View registration, Add registration, Edit registration
# Usage: View, Add, Edit registration
# Tables used: 2.4.2. Consumer - Registration
# Auther: Rohan
# Created on: 23/04/2020

class RegistrationApiView(APIView):

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

                    # Code for lookups start
                    registration = get_registration_by_id_string(request.data['id_string'])
                    country = get_country_by_id(registration.country_id)
                    state = get_state_by_id(registration.state_id)
                    city = get_city_by_id(registration.city_id)
                    area = get_area_by_id(registration.area_id)
                    sub_area = get_sub_area_by_id(registration.sub_area_id)
                    scheme = get_scheme_by_id_string(request.data["scheme_id_id_string"])
                    ownership = get_consumer_ownership_by_id_string(request.data["ownership_id_string"])
                    consumer_category = get_consumer_category_by_id(registration.consumer_category_id)
                    sub_category = get_consumer_sub_category_by_id(registration.sub_category_id)
                    registration_type = get_registration_type_by_id(registration.registration_type_id)
                    source = get_source_type_by_id(registration.source_id)
                    registration_status = get_registration_status_by_id_string(request.data["status_id_string"])
                    # Code for lookups end

                    # Code for sending registrations in response start
                    data = {
                        'tenant_id_string': registration.tenant.id_string,
                        'utility_id_string': registration.utility.id_string,
                        'registration_no': registration.registration_no,
                        'registration_type_id_string': registration_type.id_string,
                        'first_name': registration.first_name,
                        'middle_name': registration.middle_name,
                        'last_name': registration.last_name,
                        'email_id': registration.email_id,
                        'mobile_no': registration.phone_mobile,
                        'address_line_1': registration.address_line_1,
                        'street': registration.street,
                        'zipcode': registration.zipcode,
                        'country_id_string': country.id_string,
                        'state_id_string': state.id_string,
                        'city_id_string': city.id_string,
                        'area_id_string': area.id_string,
                        'sub_area_id_string': sub_area.id_string,
                        'ownership_id_string': ownership.id_string,
                        'scheme_id_string': scheme.id_string,
                        'consumer_category_id_string': consumer_category.id_string,
                        'sub_category_id_string': sub_category.id_string,
                        'status_id_string': registration_status.id_string,
                        'is_vip': registration.is_vip,
                        'connectivity': registration.connectivity,
                        'source_id_string': source.id_string,
                        'registration_date': registration.registration_date.strftime(DISPLAY_DATE_FORMAT),
                        'is_active': registration.is_active,
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
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic and payment details start
                        sid = transaction.savepoint()
                        registration, result, error = save_basic_registration_details(request, user, sid)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: error
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        payment = save_payment_details(request, user, registration, sid)
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

    def put(self, request, format=None):
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
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        registration, result, error = save_basic_registration_details(request, user)
                        if result == False:
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



class RegistrationStatusApiView(APIView):

    def get(self, request, format=None):
        try:
            registration_status_list = []
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

                    # Get registration statuses
                    registration_statuses = get_registration_statuses_by_tenant_id_string(request.data['tenant_id_string'])

                    for registration_status in registration_statuses:
                        registration_status_list.append({
                            'id_string': registration_status.id_string,
                            'name': registration_status.name
                        })
                    return Response({
                        STATE: SUCCESS,
                        'data': registration_status_list,
                    }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            pass
        except Exception as e:
            pass

    def put(self, request, format=None):
        try:
            pass
        except Exception as e:
            pass

