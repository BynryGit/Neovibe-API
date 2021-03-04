from api.messages import *
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.custom_filter_backend import CustomFilter
from v1.billing.models.bill_cycle import BillCycle as BillCycleModel
from v1.billing.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.utility.models.utility_master import get_utility_by_id_string

# API Header
# API end Point: api/v1/bill-cycle/list?utility_id_string=
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: BillCycle list
# Usage: API will fetch all Bill Cycle list
# Tables used: BillCycle
# Author: Priyanka
# Created on: 02/03/2021


class BillCycleList(generics.ListAPIView):
    try:
        serializer_class = BillCycleShortViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = BillCycleModel.objects.filter(utility=utility, is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(Bill_CYCLE_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
