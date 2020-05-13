import logging
import traceback
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.settings import DISPLAY_DATE_FORMAT
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.registration.models.registrations import Registration as RegTbl
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.models.area import get_area_by_id, get_area_by_id_string
from v1.registration.serializers.registration import RegistrationListSerializer, RegistrationViewSerializer, \
    RegistrationStatusViewSerializer
from v1.userapp.models.user_master import UserDetail
from v1.commonapp.models.city import get_city_by_id
from v1.consumer.models.consumer_category import get_consumer_category_by_id, get_consumer_category_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id, \
    get_consumer_sub_category_by_id_string
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id, get_sub_area_by_id_string
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id
from v1.consumer.models.source_type import get_source_type_by_id
from v1.registration.models.registration_status import get_registration_status_by_id, \
    get_registration_status_by_id_string
from v1.registration.models.registration_type import get_registration_type_by_id
from v1.registration.models.registrations import get_registration_by_id_string
from v1.registration.views.common_functions import is_data_verified, \
    save_payment_details, add_basic_registration_details, save_edited_basic_registration_details
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA


# API Header
# API end Point: api/v1/registrations
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Registration list
# Usage: API will fetch required data for Registration list
# Tables used: 2.4.2. Consumer - Registration
# Author: Rohan
# Created on: 21/04/2020

logger = logging.getLogger(__name__)

class RegistrationList(generics.ListAPIView):
    serializer_class = RegistrationListSerializer
    pagination_class = StandardResultsSetPagination
    # filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    # filter_fields = ('name', 'tenant__id_string',)
    # ordering_fields = ('name', 'registration_no',)
    # ordering = ('created_date',)  # always give by default alphabetical order
    # search_fields = ('name', 'email_id',)

    def get_queryset(self):
        logger.info('In api/v1/registration/list')

        queryset = RegTbl.objects.filter(registration_type_id=1)

        utility_id_string = self.request.query_params.get('utility', None)
        category_id_string = self.request.query_params.get('category', None)
        sub_category_id_string = self.request.query_params.get('sub_category', None)
        area_id_string = self.request.query_params.get('area', None)
        sub_area_id_string = self.request.query_params.get('sub_area', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        if category_id_string is not None:
            category = get_consumer_category_by_id_string(category_id_string)
            queryset = queryset.filter(consumer_category_id=category.id)
        if sub_category_id_string is not None:
            sub_category = get_consumer_sub_category_by_id_string(sub_category_id_string)
            queryset = queryset.filter(sub_category_id=sub_category.id)
        if area_id_string is not None:
            area = get_area_by_id_string(area_id_string)
            queryset = queryset.filter(area_id=area.id)
        if sub_area_id_string is not None:
            sub_area = get_sub_area_by_id_string(sub_area_id_string)
            queryset = queryset.filter(sub_area_id=sub_area.id)
        return queryset



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

class Registration(GenericAPIView):

    def get(self, request, id_string):
        try:
            registration = get_registration_by_id_string(id_string)
            if registration:
                serializer = RegistrationViewSerializer(instance=registration, context={'request': request})
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
            return Response({
                STATE: EXCEPTION,
                DATA: '',
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

                        # Save basic and payment details start
                        user = UserDetail.objects.get(id=2)
                        sid = transaction.savepoint()
                        registration, result = add_basic_registration_details(request, user, sid)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: ERROR
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        result = save_payment_details(request, user, registration, sid)
                        if result == True:
                            transaction.savepoint_commit(sid)
                        else:
                            country = get_country_by_id(registration.country_id)
                            state = get_state_by_id(registration.state_id)
                            city = get_city_by_id(registration.city_id)
                            area = get_area_by_id(registration.area_id)
                            sub_area = get_sub_area_by_id(registration.sub_area_id)
                            # scheme = get_scheme_by_id_string(request.data["scheme_id_id_string"])
                            ownership = get_consumer_ownership_by_id(registration.ownership_id)
                            consumer_category = get_consumer_category_by_id(registration.consumer_category_id)
                            sub_category = get_consumer_sub_category_by_id(registration.sub_category_id)
                            registration_type = get_registration_type_by_id(registration.registration_type_id)
                            source = get_source_type_by_id(registration.source_id)
                            registration_status = get_registration_status_by_id(registration.status_id)
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
                                'country': country.name,
                                'state_id_string': state.id_string,
                                'state': state.name,
                                'city_id_string': city.id_string,
                                'city': city.name,
                                'area_id_string': area.id_string,
                                'area': area.name,
                                'sub_area_id_string': sub_area.id_string,
                                'sub_area': sub_area.name,
                                'ownership_id_string': ownership.id_string,
                                'ownership': ownership.ownership,
                                # 'scheme_id_string': scheme.id_string,
                                'consumer_category_id_string': consumer_category.id_string,
                                'consumer_category': consumer_category.name,
                                'sub_category_id_string': sub_category.id_string,
                                'sub_category': sub_category.name,
                                'status_id_string': registration_status.id_string,
                                'status': registration_status.name,
                                'is_vip': registration.is_vip,
                                'connectivity': registration.connectivity,
                                'source_id_string': source.id_string,
                                'source': source.name,
                                'registration_date': registration.registration_date.strftime(DISPLAY_DATE_FORMAT),
                                'is_active': registration.is_active,
                            }
                            return Response({
                                STATE: SUCCESS,
                                DATA: data,
                            }, status=status.HTTP_200_OK)
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
                        user = UserDetail.objects.get(id=2)

                        registration, result = save_edited_basic_registration_details(request, user)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: ERROR
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            data = {
                                "registration_id_string": registration.id_string
                            }
                            return Response({
                                STATE: SUCCESS,
                                DATA: data,
                            }, status=status.HTTP_200_OK)
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



class RegistrationStatus(GenericAPIView):

    def get(self, request, id_string):
        try:
            registration_status = get_registration_status_by_id_string(id_string)
            if registration_status:
                serializer = RegistrationStatusViewSerializer(instance=registration_status, context={'request': request})
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
            return Response({
                STATE: EXCEPTION,
                DATA: '',
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

