import logging
import traceback
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.settings import DISPLAY_DATE_FORMAT
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.registration.models.registrations import Registration as RegTbl
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.models.area import get_area_by_id, get_area_by_id_string
from v1.registration.serializers.registration import RegistrationListSerializer, RegistrationViewSerializer, \
    RegistrationStatusViewSerializer, RegistrationSerializer
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
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS


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
class RegistrationList(generics.ListAPIView):
    serializer_class = RegistrationListSerializer
    pagination_class = StandardResultsSetPagination
    # filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    # filter_fields = ('name', 'tenant__id_string',)
    # ordering_fields = ('name', 'registration_no',)
    # ordering = ('created_date',)  # always give by default alphabetical order
    # search_fields = ('name', 'email_id',)

    def get_queryset(self):
        try:
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
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
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
                    user = UserDetail.objects.get(id = 2)
                    if is_data_verified(request):
                    # Request data verification end
                        serializer = RegistrationSerializer(data=request.data)
                        if serializer.is_valid():
                            registration_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = RegistrationViewSerializer(instance=registration_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
                            }, status=status.HTTP_201_CREATED)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
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

    def put(self, request, id_string):
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
                        registration_obj = get_registration_by_id_string(id_string)
                        if registration_obj:
                            serializer = RegistrationSerializer(instance=registration_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                            }, status=status.HTTP_404_NOT_FOUND)
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegistrationStatus(GenericAPIView):

    def get(self, request, id_string):
        try:
            registration_status = get_registration_status_by_id_string(id_string)
            if registration_status:
                serializer = RegistrationStatusViewSerializer(instance=registration_status,
                                                              context={'request': request})
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
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            pass
        except Exception as e:
            pass

    def put(self, request):
        try:
            pass
        except Exception as e:
            pass
