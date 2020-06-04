__author__ = "aki"

import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics
from master.models import User
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.tenant.serializers.bank_detail import TenantBankDetailViewSerializer, TenantBankDetailSerializer
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, DUPLICATE, DATA_ALREADY_EXISTS
from v1.tenant.models.tenant_bank_details import TenantBankDetail as TenantBankDetailTbl, \
    get_tenant_bank_details_by_id_string


# API Header
# API end Point: api/v1/tenant/id_string/bank/list
# API verb: GET
# Package: Basic
# Modules: Tenant
# Sub Module: Bank Details
# Interaction: View bank detail list
# Usage: This will display list of bank.
# Tables used: Tenant Bank Details
# Author: Gauri Deshmukh
# Created on: 20/05/2020

class TenantBankList(generics.ListAPIView):
    try:
        serializer_class = TenantBankDetailViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('bank_name',)
        ordering = ('bank_name',)  # always give by default alphabetical order
        search_fields = ('bank_name', 'branch_city' )

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = TenantBankDetailTbl.objects.filter(tenant__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/tenant/id_string/bank
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Add Tenant Bank
# Usage: Add Tenant Bank in the system
# Tables used: Tenant Bank Details
# Auther: Gauri Deshmukh
# Created on: 20/5/2020

class TenantBank (GenericAPIView):
    serializer_class = TenantBankDetailSerializer

    def post(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    tenant_obj = get_tenant_by_id_string(id_string)
                    if tenant_obj:
                        serializer = TenantBankDetailSerializer(data=request.data)
                        if serializer.is_valid():
                            tenant_bank_obj = serializer.create(serializer.validated_data, tenant_obj, user)
                            if tenant_bank_obj:
                                serializer = TenantBankDetailViewSerializer(tenant_bank_obj, context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULT: serializer.data,
                                }, status=status.HTTP_201_CREATED)
                            else:
                                return Response({
                                    STATE: DUPLICATE,
                                    RESULT: DATA_ALREADY_EXISTS,
                                }, status=status.HTTP_409_CONFLICT)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULT: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/tenant/bank/id_string
# API verb: Put,Get
# Package: Basic
# Modules: Tenant
# Sub Module: Bank
# Interaction: Get Tenant Bank , Update Tenant Bank
# Usage: Add and Update Tenant Bank in the system
# Tables used:  Tenant Bank details
# Auther: Gauri Deshmukh
# Created on: 18/5/2020

class TenantBankDetail(GenericAPIView):
    serializer_class = TenantBankDetailSerializer

    def get(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    tenant_bank_obj = get_tenant_bank_details_by_id_string(id_string)
                    if tenant_bank_obj:
                        serializer = TenantBankDetailViewSerializer(tenant_bank_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    tenant_bank_obj = get_tenant_bank_details_by_id_string(id_string)
                    if tenant_bank_obj:
                        serializer = TenantBankDetailSerializer(data=request.data)
                        if serializer.is_valid():
                            tenant_bank_obj = serializer.update(tenant_bank_obj, serializer.validated_data, user)
                            serializer = TenantBankDetailViewSerializer(tenant_bank_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULT: serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULT: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
