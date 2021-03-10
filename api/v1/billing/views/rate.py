__author__ = "priyanka"

# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.exceptions import APIException
# from rest_framework.filters import OrderingFilter, SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from v1.commonapp.views.logger import logger
# from rest_framework.generics import GenericAPIView
# from v1.utility.models.utility_master import get_utility_by_id_string
# from v1.billing.models.bill_schedule_log import ScheduleBillLog as ScheduleBillLogTbl
# from v1.commonapp.common_functions import is_token_valid, is_authorized
# from v1.commonapp.views.pagination import StandardResultsSetPagination
# from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
# from v1.billing.serializers.rate import RateShortViewSerializer
# from v1.utility.models.utility_master import get_utility_by_id_string
# from api.constants import CONSUMER_OPS, METER_DATA, VIEW
# from v1.userapp.decorators import is_token_validate, role_required
# from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, UTILITY_NOT_FOUND, SCHEDULE_LOG_NOT_FOUND
# from v1.billing.models.rate import Rate as RateTbl
# from v1.commonapp.models.product import get_product_by_id_string
# from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
# from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string

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


# class RateList(generics.ListAPIView):
#     try:
#         serializer_class = RateShortViewSerializer
#         pagination_class = StandardResultsSetPagination

#         filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
#         filter_fields = ('utility__id_string',)
#         ordering_fields = ('utility__id_string',)
#         ordering = ('utility__id_string',) # always give by default alphabetical order
#         search_fields = ('utility__name',)

#         def get_queryset(self):
#             token, user_obj = is_token_valid(self.request.headers['Authorization'])
#             if token:
#                 if is_authorized(1,1,1,user_obj):
#                     utility = get_utility_by_id_string(self.request.query_params['utility_id_string'])

#                     product = get_product_by_id_string(self.request.query_params['product_id_string']).id

#                     consumer_category = get_consumer_category_by_id_string(self.request.query_params['consumer_category__id_string']).id

#                     consumer_sub_category = get_consumer_sub_category_by_id_string(self.request.query_params['consumer_sub_category__id_string']).id

#                     queryset = RateTbl.objects.filter(utility=utility,product_id=product,consumer_category_id=consumer_category,consumer_subcategory_id=consumer_sub_category,is_active=True)
#                     return queryset
#                 else:
#                     raise InvalidAuthorizationException
#             else:
#                 raise InvalidTokenException
#     except Exception as ex:
#         logger().log(ex, 'LOW', module='Billing', sub_module='Schedule')
#         raise APIException

