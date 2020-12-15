__author__ = "aki"

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.constants import ADMIN, VIEW, TENANT, EDIT
from master.models import get_user_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.tenant.models.tenant_subscription import TenantSubscription as TenantSubscriptionTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.tenant.serializers.tenant_subscription import TenantSubscriptionViewSerializer, TenantSubscriptionSerializer
from v1.tenant.models.tenant_subscription import get_tenant_subscription_by_id_string
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT


# API Header
# API end Point: api/v1/tenant/id_string/subscription/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tenant list
# Usage: API will fetch required data for Tenant subscription list
# Tables used: 1.1 Tenant Master
# Author: Akshay
# Created on: 21/05/2020


class TenantSubscriptionList(generics.ListAPIView):
    try:
        serializer_class = TenantSubscriptionViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = TenantSubscriptionTbl.objects.filter(tenant__id_string=self.kwargs['id_string'],
                                                              is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/SUBSCRIPTION')
        raise APIException


# API Header
# API end Point: api/v1/tenant/id_string/subscription
# API verb: POST
# Package: Basic
# Modules: Tenant
# Sub Module: Subscription
# Interaction: Add Tenant Subscription
# Usage: Add Tenant Subscription in the system
# Tables used:  Tenant Subscription
# Auther: Akshay
# Created on: 21/5/2020

class TenantSubscription(GenericAPIView):
    serializer_class = TenantSubscriptionSerializer

    @is_token_validate
    @role_required(ADMIN, TENANT, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            tenant_obj = get_tenant_by_id_string(id_string)
            if tenant_obj:
                serializer = TenantSubscriptionSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_subscription_obj = serializer.create(serializer.validated_data, tenant_obj, user)
                    serializer = TenantSubscriptionViewSerializer(tenant_subscription_obj, context={'request': request})
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
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/SUBSCRIPTION')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)


# API Header
# API end Point: api/v1/tenant/subscription/:id_string
# API verb: Put,Get
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Get Tenant, Update Tenant Subscription
# Usage: Add and Update Tenant Subscription in the system
# Tables used:  Tenant Subscription
# Auther: Akshay
# Created on: 21/5/2020

class TenantSubscriptionDetail(GenericAPIView):
    serializer_class = TenantSubscriptionSerializer

    @is_token_validate
    @role_required(ADMIN, TENANT, VIEW)
    def get(self, request, id_string):
        try:
            tenant_subscription_obj = get_tenant_subscription_by_id_string(id_string)
            if tenant_subscription_obj:
                serializer = TenantSubscriptionViewSerializer(tenant_subscription_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/SUBSCRIPTION')
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
            tenant_subscription_obj = get_tenant_subscription_by_id_string(id_string)
            if tenant_subscription_obj:
                serializer = TenantSubscriptionSerializer(data=request.data)
                if serializer.is_valid():
                    tenant_subscription_obj = serializer.update(tenant_subscription_obj, serializer.validated_data, user)
                    serializer = TenantSubscriptionViewSerializer(tenant_subscription_obj, context={'request': request})
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
            logger().log(ex, 'HIGH', module='ADMIN', sub_module='TENANT/SUBSCRIPTION')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)
