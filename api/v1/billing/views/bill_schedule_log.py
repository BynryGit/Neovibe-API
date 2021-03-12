__author__ = "priyanka"

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from rest_framework.generics import GenericAPIView
from v1.billing.models.bill_schedule import get_schedule_bill_by_id_string
from v1.billing.models.bill_schedule_log import ScheduleBillLog as ScheduleBillLogTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.billing.serializers.bill_schedule_log import ScheduleBillLogViewSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from api.constants import CONSUMER_OPS, METER_DATA, VIEW
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, UTILITY_NOT_FOUND, SCHEDULE_LOG_NOT_FOUND


# API Header
# API end Point: api/v1/billing/bill-schedule-log/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: schedule log list
# Usage: API will fetch required data for schedule log list against filter and search
# Tables used: Schedule Log
# Author: Priyanka
# Created on: 10/03/2021


class ScheduleBillLogByBillSchedule(generics.ListAPIView):
    try:
        serializer_class = ScheduleBillLogViewSerializer
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
                    schedule_bill = get_schedule_bill_by_id_string(self.request.query_params['bill_schedule_id']).id
                    queryset = ScheduleBillLogTbl.objects.filter(schedule_bill_id=schedule_bill,is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='Billing', sub_module='Schedule')
        raise APIException

