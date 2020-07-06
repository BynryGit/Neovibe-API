__author__ = "aki"

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from master.models import get_user_by_id_string
from api.constants import ADMIN, VIEW, TENANT, EDIT
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_invoice_payment import get_tenant_invoice_payment_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.tenant.serializers.tenant_invoice_payment import TenantInvoicePaymentViewSerializer, \
     TenantInvoicePaymentSerializer
from v1.tenant.models.tenant_invoice_payment import TenantInvoicePayment as TenantInvoicePaymentTbl
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT


# API Header
# API end Point: api/v1/tenant/id_string/payment/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tenant Invoice Payment list
# Usage: API will fetch required data for Tenant Invoices Payment list
# Tables used: Tenant Invoice Payment
# Author: Akshay
# Created on: 21/05/2020

class TenantInvoicePaymentList(generics.ListAPIView):
    try:
        serializer_class = TenantInvoicePaymentViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name', 'invoice_number', )

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized(1,1,1,1):
                    queryset = TenantInvoicePaymentTbl.objects.filter(tenant__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/PAYMENT')
        raise APIException


# API Header
# API end Point: api/v1/tenant/id_string/payment
# API verb: POST
# Package: Basic
# Modules: Tenant
# Sub Module: Payment
# Interaction: Add Tenant Payment
# Usage: Add Tenant Payment
# Tables used:  Tenant Payment
# Auther: Akshay
# Created on: 21/5/2020

class TenantInvoicePayment(GenericAPIView):
    serializer_class = TenantInvoicePaymentSerializer

    @is_token_validate
    @role_required(ADMIN, TENANT, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            tenant_obj = get_tenant_by_id_string(id_string)
            if tenant_obj:
                serializer = TenantInvoicePaymentSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_invoice_payment_obj = serializer.create(serializer.validated_data, tenant_obj, user)
                    serializer = TenantInvoicePaymentViewSerializer(tenant_invoice_payment_obj,
                                                                    context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: serializer.data,
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/PAYMENT')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)


# API Header
# API end Point: api/v1/tenant/payment/id_string
# API verb: Put,Get
# Package: Basic
# Modules: All
# Sub Module:
# Interaction: Get Tenant, Update Tenant payment
# Usage: Add and Update Tenant Invoices Payment in the system
# Tables used:  Tenant Invoice Payment
# Auther: Akshay
# Created on: 21/5/2020

class TenantInvoicePaymentDetail(GenericAPIView):
    serializer_class = TenantInvoicePaymentSerializer

    @is_token_validate
    @role_required(ADMIN, TENANT, VIEW)
    def get(self, request, id_string):
        try:
            tenant_invoice_payment_obj = get_tenant_invoice_payment_by_id_string(id_string)
            if tenant_invoice_payment_obj:
                serializer = TenantInvoicePaymentViewSerializer(tenant_invoice_payment_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/PAYMENT')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)

    @is_token_validate
    @role_required(ADMIN, TENANT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            tenant_invoice_payment_obj = get_tenant_invoice_payment_by_id_string(id_string)
            if tenant_invoice_payment_obj:
                serializer = TenantInvoicePaymentSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_invoice_payment_obj = serializer.update(tenant_invoice_payment_obj, serializer.validated_data, user)
                    serializer = TenantInvoicePaymentViewSerializer(tenant_invoice_payment_obj, context={'request': request})
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
        except Exception as ex:
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/PAYMENT')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)
