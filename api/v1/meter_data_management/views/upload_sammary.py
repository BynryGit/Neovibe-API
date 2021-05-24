__author__ = "aki"

from rest_framework.response import Response
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
from api.constants import MX, UPLOAD, VIEW
from v1.meter_data_management.models.upload_route import UploadRoute as UploadRouteTbl
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, UTILITY_NOT_FOUND
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl


# API Header
# API end Point: api/v1/meter-data/upload/summary
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Upload route summary
# Usage: API will fetch required data for upload summary.
# Tables used: ConsumerDetailTbl, UploadRoute
# Author: Akshay
# Created on: 24/03/2021

# todo need to fix logic
class UploadSummary(generics.ListAPIView):
    @is_token_validate
    @role_required(MX, UPLOAD, VIEW)
    def get(self, request):
        try:
            if 'utility_id_string' in request.query_params:
                utility_id_string = request.query_params['utility_id_string']

                upload_summary = {
                    'total_consumer': ConsumerDetailTbl.objects.filter(utility__id_string=utility_id_string,
                                                                       is_active=True).count(),
                    'uploaded_route': UploadRouteTbl.objects.filter(utility__id_string=utility_id_string, state=3,
                                                                    is_active=True).count(),
                    'pending_route': UploadRouteTbl.objects.filter(utility__id_string=utility_id_string, state=0,
                                                                   is_active=True).count(),
                    'rejected_route': UploadRouteTbl.objects.filter(utility__id_string=utility_id_string, state=4,
                                                                    is_active=True).count(),
                }
                return Response({
                    STATE: SUCCESS,
                    RESULT: upload_summary,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: UTILITY_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='UPLOAD')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
