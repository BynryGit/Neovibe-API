__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from api.constants import ADMIN, VIEW, TENANT, EDIT
from v1.tenant.models.tenant_module import get_tenant_module_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from master.models import get_user_by_id_string
from v1.tenant.models.tenant_sub_module import TenantSubModule as TenantSubModuleTbl, get_tenant_submodule_by_id_string
from v1.tenant.serializers.tenant_sub_module import TenantSubModuleViewSerializer, TenantSubModuleSerializer


# API Header
# API end Point: api/v1/tenant/id_string/submodule/list
# API verb: GET
# Package: Basic
# Modules: Tenant
# Sub Module: SubModule
# Interaction: Tenant Submodule list
# Usage: API will fetch Tenant submodule list against single Tenant
# Tables used: 2.3 Tenant SubModule
# Author: Akshay
# Created on: 19/05/2020


class TenantSubModuleList(generics.ListAPIView):
    try:
        serializer_class = TenantSubModuleViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized(1,1,1,1):
                    queryset = TenantSubModuleTbl.objects.filter(tenant__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/SUBMODULE')
        raise APIException


# API Header
# API end Point: api/v1/tenant/module/id_string/submodule/list
# API verb: GET
# Package: Basic
# Modules: Tenant
# Sub Module: SubModule
# Interaction: Tenant Submodule list by module is_string
# Usage: API will fetch Tenant submodule list against single module
# Tables used: 2.3 Tenant SubModule
# Author: Akshay
# Created on: 14/10/2020


class TenantSubModuleListByModule(generics.ListAPIView):
    try:
        serializer_class = TenantSubModuleViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    tenant_module_obj = get_tenant_module_by_id_string(self.kwargs['id_string'])
                    print("obj",tenant_module_obj, "id",tenant_module_obj.id)
                    if tenant_module_obj:
                        queryset = TenantSubModuleTbl.objects.filter(module_id=tenant_module_obj.id, is_active=True)
                        return queryset
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/SUBMODULE')
        raise APIException


# API Header
# API end Point: api/v1/tenant/id_string/submodule
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: submodule
# Interaction: Add Tenant Submodule
# Usage: Add Tenant submodule in the system
# Tables used:  Tenant Submodule
# Auther: Akshay
# Created on: 21/5/2020

class TenantSubModule(GenericAPIView):
    serializer_class = TenantSubModuleSerializer

    @is_token_validate
    @role_required(ADMIN, TENANT, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            tenant_obj = get_tenant_by_id_string(id_string)
            if tenant_obj:
                serializer = TenantSubModuleSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_sub_module_obj = serializer.create(serializer.validated_data, tenant_obj, user)
                    serializer = TenantSubModuleViewSerializer(tenant_sub_module_obj, context={'request': request})
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
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/SUBMODULE')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)


# API Header
# API end Point: api/v1/tenant/submodule/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Tenant
# Sub Module: SubModule
# Interaction: For get and edit Tenant submodule
# Usage: API will fetch and edit Tenant submodule details
# Tables used: 1.3 Tenant SubModule
# Author: Akshay
# Created on: 20/05/2020

class TenantSubModuleDetail(GenericAPIView):
    serializer_class = TenantSubModuleSerializer

    @is_token_validate
    @role_required(ADMIN, TENANT, VIEW)
    def get(self, request, id_string):
        try:
            tenant_sub_module_obj = get_tenant_submodule_by_id_string(id_string)
            if tenant_sub_module_obj:
                serializer = TenantSubModuleViewSerializer(tenant_sub_module_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/SUBMODULE')
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
            tenant_sub_module_obj = get_tenant_submodule_by_id_string(id_string)
            if tenant_sub_module_obj:
                serializer = TenantSubModuleSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_sub_module_obj = serializer.update(tenant_sub_module_obj, serializer.validated_data, user)
                    serializer = TenantSubModuleViewSerializer(tenant_sub_module_obj, context={'request': request})
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
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/SUBMODULE')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)
