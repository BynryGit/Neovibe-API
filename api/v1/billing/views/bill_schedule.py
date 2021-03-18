__author__ = "priyanka"

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from master.models import get_user_by_id_string
from v1.commonapp.models.global_lookup import get_global_lookup_by_id_string
from v1.commonapp.views.logger import logger
from v1.utility.models.utility_master import get_utility_by_id_string
##from api.constants import CONSUMER_OPS, EDIT, METER_DATA, VIEW
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, SCHEDULE_NOT_FOUND, UTILITY_NOT_FOUND
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.billing.serializers.bill_schedule import ScheduleBillSerializer, ScheduleBillViewSerializer
from v1.billing.models.bill_schedule import ScheduleBill as ScheduleBillTbl, get_schedule_bill_by_id_string
from v1.billing.models.bill_cycle import get_bill_cycle_by_id
from v1.billing.views.common_functions import get_consumer_count, get_rate, get_additional_charges_amount



# API Header
# API end Point: api/v1/billing/schedule-bill/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: bill schedule list
# Usage: API will fetch required data for bill schedule list against filter and search
# Tables used: ScheduleBill
# Author: Priyanka
# Created on: 03/03/2021

class ScheduleBillList(generics.ListAPIView):
    try:
        serializer_class = ScheduleBillViewSerializer
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
                    queryset = ScheduleBillTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException


# API Header
# API end Point: api/v1/billing/schedule-bill
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create schedule bill object
# Usage: API will create schedule bill object based on valid data
# Tables used: ScheduleBill
# Author: Priyanka
# Created on: 03/03/2021

class ScheduleBill(GenericAPIView):
    @is_token_validate
    # #role_required(BILLING, SCHEDULE, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            # Cron Job Expression Creation Start
            if 'frequency_id' in request.data:
                frequency_obj = get_global_lookup_by_id_string(request.data['frequency_id'])
                repeat_every_obj = get_global_lookup_by_id_string(request.data['repeat_every_id'])
                if frequency_obj.key == 'daily':
                    request.data['cron_expression'] = '0 22 */' + str(repeat_every_obj.key[slice(0,1)]) + ' * *'
                if frequency_obj.key == 'weekly':
                    week_string = ''
                    for occurrence in request.data['occurs_on']:
                        occurrence_obj = get_global_lookup_by_id_string(occurrence['id_string'])
                        week_string = week_string + occurrence_obj.key + ','
                    week_string = week_string[:-1]
                    request.data['cron_expression'] = '0 22 * * ' + week_string
                if frequency_obj.key == 'monthly':
                    for occurrence in request.data['occurs_on']:
                        occurrence_obj = get_global_lookup_by_id_string(occurrence['id_string'])
                    request.data['cron_expression'] = '0 22 ' + str(occurrence_obj.key[slice(4,5)]) \
                                                      + ' */' + str(repeat_every_obj.key[slice(0,1)]) + ' *'
                if frequency_obj.key == 'yearly':
                    request.data['cron_expression'] = '0 22 1 1 *'
            # Cron Job Expression Creation End
            schedule_bill_serializer = ScheduleBillSerializer(data=request.data)
            if schedule_bill_serializer.is_valid():
                schedule_obj = schedule_bill_serializer.create(schedule_bill_serializer.validated_data, user)
                schedule_view_serializer = ScheduleBillViewSerializer(instance=schedule_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: schedule_view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: schedule_bill_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='BILLING', sub_module='Bill')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# API Header
# API end Point: api/v1/billing/schedule-bill/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View schedule bill object
# Usage: API will fetch and edit required data for schedule bill using id_string
# Tables used: Schedule
# Author: Priyank
# Created on: 04/03/2021

class ScheduleBillDetail(GenericAPIView):
    @is_token_validate
    # #role_required(CONSUMER_OPS, METER_DATA, VIEW)
    def get(self, request, id_string):
        try:
            schedule_bill_obj = get_schedule_bill_by_id_string(id_string)
            if schedule_bill_obj:
                serializer = ScheduleBillViewSerializer(instance=schedule_bill_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: SCHEDULE_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='Billing', sub_module='Bill')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    # #role_required(CONSUMER_OPS, METER_DATA, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            schedule_bill_obj = get_schedule_bill_by_id_string(id_string)
            if schedule_bill_obj:
                # Cron Job Expression Creation Start
                if 'frequency_id' in request.data:
                    frequency_obj = get_global_lookup_by_id_string(request.data['frequency_id'])
                    repeat_every_obj = get_global_lookup_by_id_string(request.data['repeat_every_id'])
                    if frequency_obj.key == 'daily':
                        request.data['cron_expression'] = '0 22 */' + str(repeat_every_obj.key[slice(0, 1)]) + ' * *'
                    if frequency_obj.key == 'weekly':
                        week_string = ''
                        for occurrence in request.data['occurs_on']:
                            occurrence_obj = get_global_lookup_by_id_string(occurrence['id_string'])
                            week_string = week_string + occurrence_obj.key + ','
                        week_string = week_string[:-1]
                        request.data['cron_expression'] = '0 22 * * ' + week_string
                    if frequency_obj.key == 'monthly':
                        for occurrence in request.data['occurs_on']:
                            occurrence_obj = get_global_lookup_by_id_string(occurrence['id_string'])
                        request.data['cron_expression'] = '0 22 ' + str(occurrence_obj.key[slice(4, 5)]) \
                                                          + ' */' + str(repeat_every_obj.key[slice(0, 1)]) + ' *'
                    if frequency_obj.key == 'yearly':
                        request.data['cron_expression'] = '0 22 1 1 *'
                # Cron Job Expression Creation End
                schedule_bill_serializer = ScheduleBillSerializer(data=request.data)
                if schedule_bill_serializer.is_valid():
                    schedule_bill_obj = schedule_bill_serializer.update(schedule_bill_obj, schedule_bill_serializer.validated_data, user)
                    schedule_view_serializer = ScheduleBillViewSerializer(instance=schedule_bill_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: schedule_view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: schedule_bill_serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: SCHEDULE_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='BILLING', sub_module='Bill')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# API Header
# API end Point: api/v1/billing/utility/<uuid:id_string>/bill-schedule-summary
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Bill Schedule summary
# Usage: API will fetch required data for bill schedule summary.
# Tables used: ScheduleBill
# Author: Priyank
# Created on: 03/03/2021

# todo need to fix logic
class BillScheduleSummary(generics.ListAPIView):
    @is_token_validate
    # #role_required(BILLING, SCHEDULE, EDIT)
    def get(self, request, id_string):
        try:
            utility_obj = get_utility_by_id_string(id_string)
            if utility_obj:
                bill_schedule_obj = ScheduleBillTbl.objects.filter(utility=utility_obj, is_active=True)
                Bill_Schedule_Count = {
                    'Total_Bill_Schedule': bill_schedule_obj.count(),
                    'New_Bill_Schedule': bill_schedule_obj.filter(schedule_status=0).count(),
                    'Complete_Bill_Schedule': bill_schedule_obj.filter(schedule_status=1).count(),
                    'Remaining_Bill_Schedule': bill_schedule_obj.filter(schedule_status=2).count(),
                }
                return Response({
                    STATE: SUCCESS,
                    RESULT: Bill_Schedule_Count,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: UTILITY_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='BILLING', sub_module='Bill')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



