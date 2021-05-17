__author__ = "aki"

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from rest_framework.generics import GenericAPIView
from v1.meter_data_management.models.schedule import get_schedule_by_id_string
from v1.meter_data_management.models.schedule_log import ScheduleLog as ScheduleLogTbl, get_schedule_log_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.meter_data_management.serializers.schedule_log import ScheduleLogViewSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from api.constants import MX, DISPATCH, VIEW
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, UTILITY_NOT_FOUND, SCHEDULE_LOG_NOT_FOUND


# API Header
# API end Point: api/v1/meter-data/schedule-log/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: schedule log list
# Usage: API will fetch required data for schedule log list against filter and search
# Tables used: Schedule Log
# Author: Akshay
# Created on: 13/01/2021


class ScheduleLogList(generics.ListAPIView):
    try:
        serializer_class = ScheduleLogViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'schedule_id')
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    self.request.query_params._mutable = True
                    if 'schedule_id' in self.request.query_params:
                        self.request.query_params['schedule_id'] = get_schedule_by_id_string(self.request.query_params['schedule_id']).id
                    self.request.query_params._mutable = False
                    queryset = ScheduleLogTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='MX', sub_module='DISPATCH')
        raise APIException


# API Header
# API end Point: api/v1/meter-data/schedule-log/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View schedule log object
# Usage: API will fetch and edit required data for schedule log using id_string
# Tables used: Schedule Log
# Author: Akshay
# Created on: 02/03/2021

class ScheduleLogDetail(GenericAPIView):
    @is_token_validate
    @role_required(MX, DISPATCH, VIEW)
    def get(self, request, id_string):
        try:
            schedule_log_obj = get_schedule_log_by_id_string(id_string)
            if schedule_log_obj:
                serializer = ScheduleLogViewSerializer(instance=schedule_log_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: SCHEDULE_LOG_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='DISPATCH')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/meter-data/utility/<uuid:id_string>/reading-schedule-log-summary
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Reading Schedule Log summary
# Usage: API will fetch required data for reading schedule summary.
# Tables used: Schedule Log
# Author: Akshay
# Created on: 1/03/2021

# todo need to fix logic
class ScheduleLogSummary(generics.ListAPIView):
    @is_token_validate
    @role_required(MX, DISPATCH, VIEW)
    def get(self, request):
        try:
            if 'utility_id_string' in request.query_params:
                utility_id_string = request.query_params['utility_id_string']
                Schedule_log_Count = {
                    'Total_Schedule_Log': ScheduleLogTbl.objects.filter(utility__id_string=utility_id_string,
                                                                        is_active=True).count(),
                    'Pending_Schedule_Log': ScheduleLogTbl.objects.filter(utility__id_string=utility_id_string,
                                                                          state=0).count(),
                    'InProgress_Schedule_Log': ScheduleLogTbl.objects.filter(utility__id_string=utility_id_string,
                                                                             state=2).count(),
                    'Complete_Schedule_Log': ScheduleLogTbl.objects.filter(utility__id_string=utility_id_string,
                                                                           state=4).count(),
                }
                return Response({
                    STATE: SUCCESS,
                    RESULT: Schedule_log_Count,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: UTILITY_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='DISPATCH')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
