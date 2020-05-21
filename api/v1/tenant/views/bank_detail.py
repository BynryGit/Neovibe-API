import traceback

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics
from v1.commonapp.views.logger import logger
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.tenant.models.tenant_bank_details import TenantMaster as tenantBankTbl, get_bank_by_id_string

from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_bank_details import get_bank_by_tenant_id_string,  get_bank_by_id
from v1.tenant.models.tenant_master import get_tenant_by_id_string, get_tenant_by_id
from v1.tenant.serializers.bank_detail import BankListSerializer, BankViewSerializer, TenantBankSerializer
from v1.tenant.views.common_functions import is_bank_data_verified, save_basic_tenant_bank_details
from v1.userapp.models.user_master import get_bank_by_user_id_string


# API Header
# API end Point: api/v1/tenant/bank/list
# API verb: GET
# Package: Basic
# Modules: Tenant
# Sub Module: Bank Details
# Interaction: View bank detail list
# Usage: This will display list of bank.
# Tables used: Tenant Bank Details
# Author: Gauri Deshmukh
# Created on: 20/05/2020

class BankList(generics.ListAPIView):
    serializer_class = BankListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('bank_name', 'id_string',)
    ordering_fields = ('bank_name', 'id_string')
    ordering = ('created_date')  # always give by default alphabetical order
    search_fields = ('bank_name', 'ifsc_no',)

    def get_queryset(self):
        queryset = tenantBankTbl.objects.filter(is_active=True)
        return queryset

    # API Header
    # API end Point: api/v1/bank
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
                        # user = UserDetail.objects.get(id = 2)
                     #   if is_data_verified(request):
                            # Request data verification end
                            duplicate_tenant_bank_obj = tenantBankTbl.objects.filter(id_string=request.data["id_string"],
                                                                            name=request.data['name'])
                            if duplicate_tenant_bank_obj:
                                return Response({
                                    STATE: DUPLICATE,
                                }, status=status.HTTP_404_NOT_FOUND)
                            else:

                                serializer = BankListSerializer(data=request.data)
                            if serializer.is_valid():
                                #                            tenant_obj = serializer.create(serializer.validated_data, user)
                                tenant_bank_obj = serializer.create(serializer.validated_data)
                                view_serializer = BankViewSerializer(instance=tenant_bank_obj,
                                                                       context={'request': request})
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
                    # else:
                    #     return Response({
                    #         STATE: ERROR,
                    #     }, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                traceback.print_exc(e)
                logger().log(e, 'ERROR', user='Tenant Exception', name='Testing')
                return Response({
                    STATE: EXCEPTION,
                    ERROR: ERROR
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API Header
# API end Point: api/v1/tenant/bank/:id_string
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
    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    tenant_bank = get_bank_by_tenant_id_string(id_string)
                    if tenant_bank:
                        serializer = Serializer(instance=tenant_bank, context={'request': request})
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
                    # if is_data_verified(request):
                        # Request data verification end
                        # Save basic details start
                        # user = UserDetail.objects.get(id=2)
                        tenant_bank_obj = get_bank_by_id_string(id_string)
                        if tenant_bank_obj:
                            serializer = TenantBankSerializer(data=request.data)
                            print("Here");
                            if serializer.is_valid(request.data):
                                tenant_obj = serializer.update(tenant_bank_obj, serializer.validated_data)
                                view_serializer = BankViewSerializer(instance=tenant_obj,
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

        except Exception as e:
            # logger().log(e, 'ERROR', user='Tenant update exception', name='Tenant')
            print("#######################",e)
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
