__author__ = "aki"

from rest_framework.response import Response
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
#from api.constants import CONSUMER_OPS, METER_DATA, VIEW
from v1.meter_data_management.models.upload_route import UploadRoute as UploadRouteTbl
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.models.utility_master import get_utility_by_id_string
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, UTILITY_NOT_FOUND
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl


# API Header
# API end Point: api/v1/meter-data/utility/<uuid:id_string>/upload-route-summary
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Upload route summary
# Usage: API will fetch required data for upload-route-summary.
# Tables used: MeterReading, UploadRoute
# Author: Akshay
# Created on: 24/03/2021

# todo need to fix logic
class UploadRouteSummary(generics.ListAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, METER_DATA, VIEW)
    def get(self, request, id_string):
        try:
            utility_obj = get_utility_by_id_string(id_string)
            if utility_obj:
                consumer_obj = ConsumerDetailTbl.objects.filter(utility=utility_obj, is_active=True).count()
                upload_route_obj = UploadRouteTbl.objects.filter(utility=utility_obj, is_active=True)
                pending_route = upload_route_obj.filter(state=0).count()
                uploaded_route = upload_route_obj.filter(state=3).count()
                rejected_route = upload_route_obj.filter(state=4).count()

                Upload_Route_Count = {
                    'total_consumer' : consumer_obj,
                    'uploaded_route' : uploaded_route,
                    'pending_route' : pending_route,
                    'rejected_route' : rejected_route,
                }
                return Response({
                    STATE: SUCCESS,
                    RESULT: Upload_Route_Count,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: UTILITY_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
