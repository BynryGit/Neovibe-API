__author__ = "aki"

from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.read_cycle import ReadCycle as ReadCycleTbl
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer


# API Header
# API end Point: api/v1/meter-data/schedule-log/:id_string/read-cycle/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: schedule log read cycle list
# Usage: API will fetch required data for schedule log route list against filter and search
# Tables used: Schedule Log, Read Cycle
# Author: Akshay
# Created on: 20/05/2021


class ScheduleLogReadCycleList(generics.ListAPIView):
    try:
        serializer_class = ReadCycleShortViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string',)
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    schedule_log_obj = get_schedule_log_by_id_string(self.kwargs['id_string'])
                    queryset = ReadCycleTbl.objects.filter(id=schedule_log_obj.read_cycle_id)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='MX', sub_module='DISPATCH')
        raise APIException
