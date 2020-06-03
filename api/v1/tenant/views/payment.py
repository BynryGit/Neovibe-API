import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_invoice_payment import TenantInvoicePayment as tenantInvoicesPaymentTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.tenant.serializers.payment import TenantInvoicePaymentListSerializer, TenantInvoicePaymentViewSerializer, \
     TenantInvoicePaymentSerializer
from v1.tenant.models.tenant_invoice_payment import get_tenant_payment_by_id_string
from v1.tenant.views.common_functions import is_data_verified, is_payment_data_verified
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS, DUPLICATE


# API Header
# API end Point: api/v1/tenant/payment/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tenant Invoice Payment list
# Usage: API will fetch required data for Tenant Invoices Payment list
# Tables used: Tenant Invoice Payment
# Author: Gauri Deshmukh
# Created on: 21/05/2020

class TenantInvoicePaymentList(generics.ListAPIView):
    serializer_class = TenantInvoicePaymentListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('invoice_number', 'id_string',)
    ordering_fields = ('invoice_number', 'id_string')
    ordering = ('created_date')  # always give by default alphabetical order
    search_fields = ('invoice_number')

    def get_queryset(self):
        queryset = tenantInvoicesPaymentTbl.objects.filter(is_active=True)
        return queryset


#
# # API Header
# # API end Point: api/v1/tenant/payment
# # API verb: POST
# # Package: Basic
# # Modules: Tenant
# # Sub Module: Payment
# # Interaction: Add Tenant Payment
# # Usage: Add Tenant Payment
# # Tables used:  Tenant Payment
# # Auther: Gauri Deshmukh
# # Created on: 21/5/2020

class TenantInvoicePayment(GenericAPIView):

    def post(self, request):
        try:
            # Checking authentication start
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    #user = User.objects.get(id = 2)
                    if is_payment_data_verified(request):
                    # Request data verification end
                        duplicate_tenant_invoice_payment_obj = tenantInvoicesPaymentTbl.objects.filter(invoice_number=request.data['invoice_number'])
                        if duplicate_tenant_invoice_payment_obj:
                            return Response({
                                STATE: DUPLICATE,
                            }, status=status.HTTP_404_NOT_FOUND)
                        else:
                            serializer = TenantInvoicePaymentSerializer(data=request.data)
                        if serializer.is_valid():
#                            tenant_obj = serializer.create(serializer.validated_data, user)
                            tenant_invoice_payment_obj = serializer.create(serializer.validated_data)
                            view_serializer = TenantInvoicePaymentViewSerializer(instance=tenant_invoice_payment_obj, context={'request': request})
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
            logger().log(e, 'ERROR', user='Exception', name='Testing')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API Header
# API end Point: api/v1/tenant/payment
# API verb: Put,Get
# Package: Basic
# Modules: All
# Sub Module:
# Interaction: Get Tenant, Update Tenant payment
# Usage: Add and Update Tenant Invoices Payment in the system
# Tables used:  Tenant Invoice Payment
# Auther: Gauri Deshmukh
# Created on: 21/5/2020

class TenantInvoicePaymentDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    tenant_invoice_payment = get_tenant_payment_by_id_string(id_string)
                    if tenant_invoice_payment:
                        serializer = TenantInvoicePaymentViewSerializer(instance=tenant_invoice_payment, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # logger().log(e, 'ERROR', user='Get Tenant Exception ', name='Tenant issue')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(1):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_payment_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        # user = User.objects.get(id=2)
                        tenant_invoice_payment_obj = get_tenant_payment_by_id_string(id_string)

                        if tenant_invoice_payment_obj:
                            serializer = TenantInvoicePaymentSerializer(data=request.data)
                            print("Here");
                            if serializer.is_valid(request.data):

                                tenant_invoice_payment_obj = serializer.update(tenant_invoice_payment_obj, serializer.validated_data)

                                view_serializer = TenantInvoicePaymentViewSerializer(instance=tenant_invoice_payment_obj,
                                                                             context={'request': request})
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
            # logger().log(e, 'ERROR', user='Tenant update exception', name='Tenant')
            print("#######################",e)
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


