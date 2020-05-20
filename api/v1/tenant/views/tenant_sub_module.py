__author__ = "Gauri"

import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.user_master import UserDetail
from v1.tenant.models.tenant_sub_module import get_tenant_submodule_by_id_string, TenantSubModule as TenantSubModuleTbl
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
# Author: Gauri
# Created on: 19/05/2020


class TenantSubModuleList(generics.ListAPIView):
    serializer_class = TenantSubModuleViewSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('tenant__id_string')
    ordering_fields = ('submodule_name', 'tenant_name')
    ordering = ('submodule_name',)  # always give by default alphabetical order
    search_fields = ('submodule_name', 'tenant_name')

    def get_queryset(self):
        if is_token_valid(self.request.headers['token']):
            if is_authorized():
                queryset = TenantSubModuleTbl.objects.filter(tenant__id_string=self.kwargs['tenant'], is_active=True)
                return queryset
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                STATE: ERROR,
            }, status=status.HTTP_401_UNAUTHORIZED)


# API Header
# API end Point: api/v1/tenant/submodule/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Tenant
# Sub Module: SubModule
# Interaction: For get and edit Tenant submodule
# Usage: API will fetch and edit Tenant submodule details
# Tables used: 1.3 Tenant SubModule
# Author: Gauri Deshmukh
# Created on: 20/05/2020

class TenantSubModuleDetail(GenericAPIView):
    serializer_class = TenantSubModuleSerializer

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

                    tenant_submodule_obj = get_tenant_submodule_by_id_string(id_string)
                    if tenant_submodule_obj:
                        serializer = TenantSubModuleViewSerializer(tenant_submodule_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: serializer.data,
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
                    user = UserDetail.objects.get(id=2)
                    # Todo fetch user from request end

                    tenant_submodule_obj = get_tenant_submodule_by_id_string(id_string)
                    if tenant_submodule_obj:
                        serializer = TenantSubModuleSerializer(data=request.data)
                        if serializer.is_valid():
                            tenant_submodule_obj = serializer.update(tenant_submodule_obj, serializer.validated_data, user)
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: {'tenant_submodule_obj': tenant_submodule_obj.id_string},
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
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