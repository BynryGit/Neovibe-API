__author__ = "aki"

from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.schedule import get_schedule_by_id_string
from v1.meter_data_management.models.schedule_log import ScheduleLog as ScheduleLogTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.meter_data_management.serializers.validation_schedule_log import ValidationScheduleLogViewSerializer


# API Header
# API end Point: api/v1/meter-data/validation-schedule-log/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: validation schedule log log list
# Usage: API will fetch required data for validation schedule log list against filter and search
# Tables used: Schedule Log
# Author: Akshay
# Created on: 15/03/2021


class ValidationScheduleLogList(generics.ListAPIView):
    try:
        serializer_class = ValidationScheduleLogViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'schedule_id')
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_serializer_context(self):
            """
            Extra context provided to the serializer class.
            """
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            return {
                'user_id_string': user_obj,
            }

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
        logger().log(ex, 'LOW', module='MX', sub_module='VALIDATION')
        raise APIException
