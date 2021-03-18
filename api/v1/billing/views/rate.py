__author__ = "priyanka"

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from rest_framework.generics import GenericAPIView
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.billing.models.bill_schedule_log import ScheduleBillLog as ScheduleBillLogTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.billing.serializers.rate import RateShortViewSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
#from api.constants import CONSUMER_OPS, METER_DATA, VIEW
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, UTILITY_NOT_FOUND, SCHEDULE_LOG_NOT_FOUND
from v1.billing.models.rate import Rate as RateTbl, get_rate_by_category_sub_category_wise
from v1.billing.models.bill_schedule import get_schedule_bill_by_id_string
from v1.billing.models.bill_cycle import get_bill_cycle_by_id
from v1.meter_data_management.models.route import get_route_by_id_string
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_premise_id
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id
from v1.commonapp.models.premises import get_premise_by_id_string


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


class RateList(GenericAPIView):
    def get(self, request, id_string):
        try:
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    bill_shedule_obj = get_schedule_bill_by_id_string(id_string)
                    bill_cycle_obj = get_bill_cycle_by_id(bill_shedule_obj.bill_cycle_id)
                    for route in bill_cycle_obj.route_json:
                        route_obj = get_route_by_id_string(route['id_string'])
                        for premise in route_obj.premises_json:
                            premise_obj = get_premise_by_id_string(premise['id_string'])
                            consumer_meter_obj = get_consumer_service_contract_detail_by_premise_id(premise_obj.id)
                            contract_obj = get_utility_service_contract_master_by_id(consumer_meter_obj.service_contract_id)
                    rate_obj = get_rate_by_category_sub_category_wise(bill_shedule_obj.utility,bill_shedule_obj.utility_product_id,contract_obj.consumer_category_id,contract_obj.consumer_sub_category_id)
                    serializer = RateShortViewSerializer(instance=rate_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: SCHEDULE_NOT_FOUND,
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                raise InvalidTokenException
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='Billing', sub_module='Bill')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    