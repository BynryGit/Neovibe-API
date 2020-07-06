__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.constants import ADMIN, VIEW, TENANT, EDIT
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.tenant.serializers.tenant_module import TenantModuleViewSerializer, TenantModuleSerializer
from master.models import get_user_by_id_string
from v1.tenant.models.tenant_module import TenantModule as TenantModuleTbl, get_tenant_module_by_id_string


# API Header
# API end Point: api/v1/tenant/id_string/module/list
# API verb: GET
# Package: Basic
# Modules: Tenant
# Sub Module: Module
# Interaction: Tenant module list
# Usage: API will fetch Tenant module list against single Tenant
# Tables used: TenantModule
# Author: Akshay
# Created on: 03/06/2020


class TenantModuleList(generics.ListAPIView):
    try:
        serializer_class = TenantModuleViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name', )

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized(1,1,1,1):
                    queryset = TenantModuleTbl.objects.filter(tenant__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/MODULE')
        raise APIException


# API Header
# API end Point: api/v1/tenant/id_string/module
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: module
# Interaction: Add Tenant module
# Usage: Add Tenant module in the system
# Tables used: TenantModule
# Auther: Akshay
# Created on: 03/06/2020

class TenantModule(GenericAPIView):
    serializer_class = TenantModuleSerializer

    @is_token_validate
    @role_required(ADMIN, TENANT, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            tenant_obj = get_tenant_by_id_string(id_string)
            if tenant_obj:
                serializer = TenantModuleSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_module_obj = serializer.create(serializer.validated_data, tenant_obj, user)
                    serializer = TenantModuleViewSerializer(tenant_module_obj, context={'request': request})
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
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/MODULE')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)


# API Header
# API end Point: api/v1/tenant/module/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Tenant
# Sub Module: Module
# Interaction: For get and edit Tenant module
# Usage: API will fetch and edit Tenant module details
# Tables used: TenantModule
# Author: Akshay
# Created on: 03/06/2020

class TenantModuleDetail(GenericAPIView):
    serializer_class = TenantModuleSerializer

    @is_token_validate
    @role_required(ADMIN, TENANT, VIEW)
    def get(self, request, id_string):
        try:
            tenant_module_obj = get_tenant_module_by_id_string(id_string)
            if tenant_module_obj:
                serializer = TenantModuleViewSerializer(tenant_module_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/MODULE')
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
            tenant_module_obj = get_tenant_module_by_id_string(id_string)
            if tenant_module_obj:
                serializer = TenantModuleSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_module_obj = serializer.update(tenant_module_obj, serializer.validated_data, user)
                    serializer = TenantModuleViewSerializer(tenant_module_obj, context={'request': request})
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
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/MODULE')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)
