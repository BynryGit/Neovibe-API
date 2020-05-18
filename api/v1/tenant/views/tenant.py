import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_master import TenantMaster as tenantTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.registration.serializers.registration import RegistrationListSerializer, RegistrationViewSerializer, \
    RegistrationStatusViewSerializer, RegistrationSerializer
from v1.tenant.serializers.tenant import TenantSerializer,TenantMaster
from v1.userapp.models.user_master import UserDetail
from v1.tenant.models.tenant_status import get_tenant_status_by_id
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.tenant.views.common_functions import is_data_verified
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS


# API Header
# API end Point: api/v1/tenants
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Utilities list
# Usage: API will fetch required data for Utilities list
# Tables used: 1.1 Utility Master
# Author: Gauri Deshmukh
# Created on: 18/05/2020

class UtilityList(generics.ListAPIView):
    serializer_class = RegistrationListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('first_name', 'tenant__id_string',)
    ordering_fields = ('first_name', 'tenant_id')
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('first_name', 'email_id',)

    def get_queryset(self):
        queryset = tenantTbl.objects.filter(is_active=True)
        return queryset



# API Header
# API end Point: api/v1/tenant
# API verb: GET, POST, PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View Tenant, Add Tenant, Edit Tenant
# Usage: View, Add, Edit Tenant
# Tables used: 1.1. Tenant master
# Auther: Gauri Deshmukh
# Created on: 18/5/2020
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
            traceback.print_exc(e)
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
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
                        user = UserDetail.objects.get(id=2)
                        registration_obj = get_registration_by_id_string(id_string)
                        if registration_obj:
                            serializer = RegistrationSerializer(data=request.data)
                            if serializer.is_valid(request.data):
                                registration_obj = serializer.update(registration_obj,serializer.validated_data, user)
                                view_serializer = RegistrationViewSerializer(instance=registration_obj, context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULTS: view_serializer.data,
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
            # logger().log(e, 'ERROR', user='test', name='test')
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
