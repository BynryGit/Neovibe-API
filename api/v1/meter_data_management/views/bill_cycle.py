__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.meter_data_management.models.bill_cycle import get_bill_cycle_by_id_string
from v1.meter_data_management.serializers.bill_cycle import BillCycleViewSerializer
from v1.meter_data_management.models.bill_cycle import BillCycle as BillCycleTbl


# API Header
# API end Point: api/v1/meter-data/bill-cycle/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: bill-cycle list
# Usage: API will fetch required data for bill-cycle list against filter and search
# Tables used: 2.12.23 Bill Cycle
# Author: Akshay
# Created on: 12/06/2020

class BillCycleList(generics.ListAPIView):
    try:
        serializer_class = BillCycleViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('code', 'utility__id_string',)
        ordering_fields = ('code', 'utility__id_string',)
        ordering = ('code',) # always give by default alphabetical order
        search_fields = ('code', 'utility__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = BillCycleTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/bill-cycle/id_string
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View bill-cycle object
# Usage: API will fetch required data for bill-cycle using id_string
# Tables used: 2.12.23 Bill Cycle
# Author: Akshay
# Created on: 12/06/2020

class BillCycleDetail(GenericAPIView):
    serializer_class = BillCycleViewSerializer

    def get(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end

                    bill_cycle_obj = get_bill_cycle_by_id_string(id_string)
                    if bill_cycle_obj:
                        serializer = BillCycleViewSerializer(instance=bill_cycle_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
