import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from master.models import User
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_invoice import TenantInvoice as TenantInvoiceTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.tenant.serializers.tenant_invoice import TenantInvoiceViewSerializer, TenantInvoiceSerializer
from v1.tenant.models.tenant_invoice import get_tenant_invoice_by_id_string
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, DUPLICATE, DATA_ALREADY_EXISTS


# API Header
# API end Point: api/v1/tenant/id_string/invoice/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tenant Invoice list
# Usage: API will fetch required data for Tenant Invoices list
# Tables used: Tenant Invoice
# Author: Akshay
# Created on: 21/05/2020

class TenantInvoiceList(generics.ListAPIView):
    try:
        serializer_class = TenantInvoiceViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name', 'invoice_number', )

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = TenantInvoiceTbl.objects.filter(tenant__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/tenant/id_string/invoice
# API verb: POST
# Package: Basic
# Modules: Tenant
# Sub Module: Invoice
# Interaction: Add Tenant invoice
# Usage: Add Tenant invoice in the system
# Tables used:  Tenant invoice
# Auther: Akshay
# Created on: 21/5/2020

class TenantInvoice(GenericAPIView):
    serializer_class = TenantInvoiceSerializer

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
                        serializer = TenantInvoiceSerializer(data=request.data)
                        if serializer.is_valid():
                            tenant_invoice_obj = serializer.create(serializer.validated_data, tenant_obj, user)
                            if tenant_invoice_obj:
                                serializer = TenantInvoiceViewSerializer(tenant_invoice_obj, context={'request': request})
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
# API end Point: api/v1/tenant/invoice/id_string
# API verb: Put,Get
# Package: Basic
# Modules: All
# Sub Module:
# Interaction: Get, Update Tenant Invoice
# Usage: Add and Update Tenant Invoices in the system
# Tables used:  Tenant Invoice
# Auther: Akshay
# Created on: 21/5/2020

class TenantInvoiceDetail(GenericAPIView):
    serializer_class = TenantInvoiceSerializer

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

                    tenant_invoice_obj = get_tenant_invoice_by_id_string(id_string)
                    if tenant_invoice_obj:
                        serializer = TenantInvoiceViewSerializer(tenant_invoice_obj, context={'request': request})
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

                    tenant_invoice_obj = get_tenant_invoice_by_id_string(id_string)
                    if tenant_invoice_obj:
                        serializer = TenantInvoiceSerializer(data=request.data)
                        if serializer.is_valid():
                            tenant_invoice_obj = serializer.update(tenant_invoice_obj, serializer.validated_data, user)
                            serializer = TenantInvoiceViewSerializer(tenant_invoice_obj, context={'request': request})
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