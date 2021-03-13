__author__ = "aki"

from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl
from v1.meter_data_management.serializers.schedule_log_read_cycle_revisit_task import \
    ScheduleLogReadCycleRevisitTaskViewSerializer

# API Header
# API end Point: api/v1/meter-data/schedule-log/:id_string/read-cycle-revisit-task/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: schedule log read cycle revisit task list
# Usage: API will fetch required data for schedule log read cycle revisit task
# Tables used: Schedule Log, Schedule, Read Cycle
# Author: Akshay
# Created on: 12/03/2021


class ScheduleLogReadCycleRevisitTaskList(generics.ListAPIView):
    try:
        serializer_class = ScheduleLogReadCycleRevisitTaskViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string',)
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_serializer_context(self):
            """
            Extra context provided to the serializer class.
            """
            return {
                'schedule_log_id': self.kwargs['id_string'],
            }

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    schedule_log_obj = get_schedule_log_by_id_string(self.kwargs['id_string'])
                    route_task_assignment_obj = RouteTaskAssignmentTbl.objects.filter(schedule_log_id=schedule_log_obj.id,
                                                                                      read_cycle_id=schedule_log_obj.read_cycle_id,
                                                                                      consumer_meter_json__contains=
                                                                                      [{'is_active': True},
                                                                                       {'is_revisit': True}],
                                                                                      is_active=True)
                    return route_task_assignment_obj
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException
