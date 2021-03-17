__author__ = "aki"

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
##from api.constants import ADMIN, TENANT, VIEW, EDIT
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_master import TenantMaster as TenantMasterTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.tenant.serializers.tenant import TenantMasterViewSerializer
from v1.tenant.serializers.tenant import TenantMasterSerializer
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULT
from master.models import get_user_by_id_string


# API Header
# API end Point: api/v1/tenant/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tenant list
# Usage: API will fetch required data for Tenant list
# Tables used: 1.1 Tenant Master
# Author: Akshay
# Created on: 18/05/2020


class TenantList(generics.ListAPIView):
    try:
        serializer_class = TenantMasterViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'id_string',)
        ordering_fields = ('name', 'id_string',)
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'email_id',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['Authorization']):
                if is_authorized(1,1,1,1):
                    queryset = TenantMasterTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT')
        raise APIException


# API Header
# API end Point: api/v1/tenant
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Add Tenant
# Usage: Add Tenant in the system
# Tables used: 1.1. Tenant master
# Auther: Akshay
# Created on: 18/5/2020

class Tenant(GenericAPIView):

    # @is_token_validate
    # #role_required(ADMIN, TENANT, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            serializer = TenantMasterSerializer(data=request.data)
            if serializer.is_valid():
                tenant_obj = serializer.create(serializer.validated_data, user)
                serializer = TenantMasterViewSerializer(instance=tenant_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)


# API Header
# API end Point: api/v1/tenant/:id_string
# API verb: Put,Get
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Get Tenant, Update Tenant
# Usage: Add and Update Tenant in the system
# Tables used: 1.1. Tenant master
# Auther: Akshay
# Created on: 18/5/2020

class TenantDetail(GenericAPIView):
    @is_token_validate
    #role_required(ADMIN, TENANT, VIEW)
    def get(self, request, id_string):
        try:
            tenant_obj = get_tenant_by_id_string(id_string)
            if tenant_obj:
                serializer = TenantMasterViewSerializer(instance=tenant_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)

    @is_token_validate
    #role_required(ADMIN, TENANT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            tenant_obj = get_tenant_by_id_string(id_string)
            if tenant_obj:
                serializer = TenantMasterSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_obj = serializer.update(tenant_obj, serializer.validated_data, user)
                    serializer = TenantMasterViewSerializer(instance=tenant_obj, context={'request': request})
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
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)
