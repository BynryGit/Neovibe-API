__author__ = "priyanka"

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.models.global_lookup import get_global_lookup_by_id_string
from v1.commonapp.views.logger import logger
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, SCHEDULE_NOT_FOUND, UTILITY_NOT_FOUND
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.userapp.decorators import is_token_validate, role_required
from v1.billing.models.bill_schedule import ScheduleBill as ScheduleBillTbl, get_schedule_bill_by_id_string
from v1.billing.models.bill_cycle import get_bill_cycle_by_id
from v1.billing.views.common_functions import get_consumer_count, get_rate, get_additional_charges_amount,\
     get_reading_count,calculate_current_all_charges
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from master.models import get_user_by_id_string
from v1.billing.models.bill_schedule_log import get_schedule_bill_log_by_schedule_id
from v1.billing.models.bill_consumer_detail import get_bill_consumer_detail_by_schedule_log_id
from v1.billing.serializers.bill import ScheduleBillConsumerViewSerializer
from api.messages import *
from api.constants import *
from v1.commonapp.views.pagination import StandardResultsSetPagination

# API Header
# API end Point: api/v1/billing/get-charges/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View all details before run bill
# Usage: API will fetch all details before run bill for schedule bill using id_string
# Tables used: Schedule
# Author: Priyank
# Created on: 14/03/2021

class GetAllChargesDetails(GenericAPIView):
    @is_token_validate
    # #role_required(CONSUMER_OPS, METER_DATA, VIEW)
    def get(self, request, id_string):
        try:
            data=[]
            summary = {}
            detail_value={}
            schedule_bill_obj = get_schedule_bill_by_id_string(id_string)
            detail_value['schedule_bill_id_string'] = schedule_bill_obj.id_string
            detail_value['name'] = schedule_bill_obj.name
            detail_value['bill_cycle_name'] = get_bill_cycle_by_id(schedule_bill_obj.bill_cycle_id).bill_cycle_name
            detail_value['start_date'] = schedule_bill_obj.start_date
            detail_value['end_date'] = schedule_bill_obj.end_date

            # it's getting total consumer count
            detail_value['consumer_count'] = get_consumer_count(schedule_bill_obj.id)
            # it's getting rate according to Consumer category subcategory wise
            detail_value['rate'] =  get_rate(schedule_bill_obj)
            # it's getting total reading count
            detail_value['reading_count'] = get_reading_count(schedule_bill_obj)
            # it's getting total consumer count
            additional_val =  get_additional_charges_amount(schedule_bill_obj)            
            detail_value['meter_status'] =  additional_val['meter_status']
            detail_value['outstanding_amount'] =  additional_val['outstanding']
            detail_value['additional_charges'] =  additional_val['additional_charges']
            
            data.append(detail_value)
            if data:
                return Response({
                    STATE: SUCCESS,
                    RESULT: data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: SCHEDULE_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print('-----ex---GetAllChargesDetails----',ex)
            logger().log(ex, 'MEDIUM', module='Billing', sub_module='Bill')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SaveBillCharges(GenericAPIView):
    @is_token_validate
    # #role_required(BILLING, SCHEDULE, EDIT)
    def post(self, request):
        try:
            data = {}
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            calculate_current_all_charges(request.data)
            data['schedule_bill_id_string'] = request.data['schedule_bill_id_string']
            return Response({
                    STATE: SUCCESS,
                    RESULT: data,
                }, status=status.HTTP_200_OK)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='Billing', sub_module='Bill')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetBillConsumerDetails(generics.ListAPIView):
    
    try:
        serializer_class = ScheduleBillConsumerViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('tenant__id_string',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    schedule_bill_obj = get_schedule_bill_by_id_string(self.kwargs['schedule_bill_id_string'])
                    if schedule_bill_obj:
                        schedule_log_id = get_schedule_bill_log_by_schedule_id(schedule_bill_obj.id)
                        if schedule_log_id:
                            queryset = get_bill_consumer_detail_by_schedule_log_id(schedule_log_id.id)
                            if queryset:
                                return queryset
                            else:
                                raise CustomAPIException("User not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        print('..........',e)
        logger().log(e, 'MEDIUM', module='BX', sub_module='Billing')



