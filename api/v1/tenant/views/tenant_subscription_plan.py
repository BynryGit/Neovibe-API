__author__ = "aki"

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.tenant.models.tenant_subscription_plan import TenantSubscriptionPlan as TenantSubscriptionPlanTbl
from v1.tenant.serializers.tenant_subscription_plan import TenantSubscriptionPlanViewSerializer


# API Header
# API end Point: api/v1/tenant/subscription-plan/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: subscription plan list
# Usage: API will fetch required data for subscription plan list
# Tables used: 1.2 Tenant Subscription Plan
# Author: Akshay
# Created on: 04/06/2020


class TenantSubscriptionPlanList(generics.ListAPIView):
    try:
        serializer_class = TenantSubscriptionPlanViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('id_string',)
        ordering_fields = ('id_string',)
        ordering = ('subscription_name',)  # always give by default alphabetical order
        search_fields = ('subscription_name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized(1,1,1,1):
                    queryset = TenantSubscriptionPlanTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/SUBSCRIPTION-PLAN')
        raise APIException
