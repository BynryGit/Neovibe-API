__author__ = "aki"

from rest_framework.response import Response
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
from api.constants import MX, VALIDATION, VIEW
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, UTILITY_NOT_FOUND
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl


# API Header
# API end Point: api/v1/meter-data/validation/summary
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: validation summary
# Usage: API will fetch required data for validation-summary.
# Tables used: MeterReading, ConsumerDetail
# Author: Akshay
# Created on: 15/03/2021

# todo need to fix logic
class ValidationSummary(generics.ListAPIView):
    @is_token_validate
    @role_required(MX, VALIDATION, VIEW)
    def get(self, request):
        try:
            if 'utility_id_string' in request.query_params:
                utility_id_string = request.query_params['utility_id_string']
                total_completed_task = 0
                consumer_obj = ConsumerDetailTbl.objects.filter(utility__id_string=utility_id_string,
                                                                is_active=True).count()
                route_task_assignment_obj = RouteTaskAssignmentTbl.objects.filter(utility__id_string=utility_id_string,
                                                                                  is_active=True)

                for route_task in route_task_assignment_obj:
                    complete_task_obj = [x for x in route_task.consumer_meter_json if x['is_active'] == True and
                                         x['is_completed'] == True and x['is_revisit'] == False]
                    total_completed_task = total_completed_task + len(complete_task_obj)

                validation_summary = {
                    'total_consumer': consumer_obj,
                    'reading_received': total_completed_task,
                    'pending_reading': consumer_obj - total_completed_task,
                    'total_revisit': MeterReadingTbl.objects.filter(utility__id_string=utility_id_string,
                                                                    reading_status=3, is_active=False).count(),
                    'total_duplicate': MeterReadingTbl.objects.filter(utility__id_string=utility_id_string,
                                                                      is_duplicate=True, is_active=False).count(),
                    'validation_one': MeterReadingTbl.objects.filter(utility__id_string=utility_id_string,
                                                                     reading_status=0, is_assign_to_v1=True,
                                                                     is_active=True).count(),
                    'validation_two': MeterReadingTbl.objects.filter(utility__id_string=utility_id_string,
                                                                     reading_status=1, is_assign_to_v2=True,
                                                                     is_active=True).count(),
                    'completed_reading': MeterReadingTbl.objects.filter(utility__id_string=utility_id_string,
                                                                        reading_status=2, is_active=True).count(),
                }
                return Response({
                    STATE: SUCCESS,
                    RESULT: validation_summary,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: UTILITY_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='VALIDATION')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
