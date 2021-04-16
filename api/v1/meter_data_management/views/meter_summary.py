__author__ = "aki"

from rest_framework.response import Response
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.meter import Meter as MeterTbl
from v1.utility.models.utility_master import get_utility_by_id_string
from api.constants import MX, METER_MASTER, VIEW
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, UTILITY_NOT_FOUND


# API Header
# API end Point: api/v1/meter-data/utility/<uuid:id_string>/meter-summary
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter summary
# Usage: API will fetch required data for meter-summary.
# Tables used: Meter
# Author: Akshay
# Created on: 19/02/2021

# todo need to fix logic
class MeterSummary(generics.ListAPIView):
    @is_token_validate
    @role_required(MX, METER_MASTER, VIEW)
    def get(self, request, id_string):
        try:
            utility_obj = get_utility_by_id_string(id_string)
            if utility_obj:
                meter_obj = MeterTbl.objects.filter(utility=utility_obj, is_active=True)
                Meter_Count = {
                    'Total_Meter' : meter_obj.count(),
                    'Normal_Meter' : meter_obj.filter(meter_status=0).count(),
                    'Faulty_Meter' : meter_obj.filter(meter_status=1).count(),
                    'RCNT_Meter' : meter_obj.filter(meter_status=2).count(),
                }
                return Response({
                    STATE: SUCCESS,
                    RESULT: Meter_Count,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: UTILITY_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='METER_MASTER')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
