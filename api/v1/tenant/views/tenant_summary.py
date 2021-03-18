__author__ = "aki"

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from v1.userapp.decorators import is_token_validate, role_required
#from api.constants import ADMIN, TENANT, VIEW
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from v1.commonapp.views.logger import logger
from v1.tenant.serializers.tenant_summary import TenantSummaryOnMonthlyBasisViewSerializer
from v1.tenant.models.tenant_summary_on_monthly_basis import get_tenant_usage_summary_by_tenant_id_string


# API Header
# API end Point: api/v1/tenant/id_string/summary
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tenant summary
# Usage: API will fetch all summary against tenant
# Tables used: Tenant Usage Summary
# Author: Akshay
# Created on: 20/05/2020


class TenantSummaryDetail(GenericAPIView):
    serializer_class = TenantSummaryOnMonthlyBasisViewSerializer

    @is_token_validate
    #role_required(ADMIN, TENANT, VIEW)
    def get(self, request, id_string):
        try:
            tenant_summary_obj = get_tenant_usage_summary_by_tenant_id_string(id_string)
            if tenant_summary_obj:
                serializer = TenantSummaryOnMonthlyBasisViewSerializer(tenant_summary_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/SUMMARY')
            response = self.handle_exception(ex)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=response.status_code)
