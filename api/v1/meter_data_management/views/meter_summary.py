__author__ = "aki"

from rest_framework.response import Response
from rest_framework import generics, status
from v1.commonapp.models.meter_status import get_meter_status_by_name
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.meter import Meter as MeterTbl
from api.constants import MX, METER_MASTER, VIEW
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, UTILITY_NOT_FOUND


# API Header
# API end Point: api/v1/meter-data/meter/summary
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
    def get(self, request):
        try:
            if 'utility_id_string' in request.query_params:
                utility_id_string = request.query_params['utility_id_string']

                meter_summary = {
                    'Total_Meter': MeterTbl.objects.filter(utility__id_string=utility_id_string,
                                                           is_active=True).count(),
                    'Normal_Meter': MeterTbl.objects.filter(utility__id_string=utility_id_string,
                                                            meter_status=get_meter_status_by_name(name='Normal').id,
                                                            is_active=True).count(),
                    'Faulty_Meter': MeterTbl.objects.filter(utility__id_string=utility_id_string,
                                                            meter_status=get_meter_status_by_name(name='Faulty').id,
                                                            is_active=True).count(),
                    'RCNT_Meter': MeterTbl.objects.filter(utility__id_string=utility_id_string,
                                                          meter_status=get_meter_status_by_name(name='RCNT').id,
                                                          is_active=True).count(),
                }
                return Response({
                    STATE: SUCCESS,
                    RESULT: meter_summary,
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
