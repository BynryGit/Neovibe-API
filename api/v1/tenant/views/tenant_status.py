from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.views.logger import logger
from v1.tenant.serializers.tenant import TenantStatusViewSerializer
from v1.tenant.models.tenant_status import get_tenant_status_by_id
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS

# API Header
# API end Point: api/v1/tenant/status
# API verb: GET
# Package: Basic
# Modules: Tenant
# Sub Module: All
# Interaction: Get Tenant Status
# Usage: API will fetch required data to get Tenant Status
# Tables used: Tenant Status
# Author: Gauri Deshmukh
# Created on: 18/05/2020

class TenantStatus(GenericAPIView):

    def get(self, request, id_string):
        try:
            tenant_status = get_tenant_status_by_id(id_string)
            if tenant_status:
                serializer = TenantStatusViewSerializer(instance=tenant_status, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger().log(e, 'ERROR', user='status test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            pass
        except Exception as e:
            pass

    def put(self, request):
        try:
            pass
        except Exception as e:
            pass
