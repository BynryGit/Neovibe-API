__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from xlrd import open_workbook
from django_filters.rest_framework import DjangoFilterBackend
from api.messages import STATE, ERROR, EXCEPTION
from api.constants import CONSUMER_OPS, EDIT, METER_DATA
from master.models import get_user_by_id_string
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.userapp.decorators import is_token_validate, role_required
from v1.meter_data_management.models.meter import Meter as MeterTbl
from v1.meter_data_management.serializers.meter import MeterViewSerializer


# API Header
# API end Point: api/v1/meter-data/meter/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter list
# Usage: API will fetch required data for meter list against filter and search
# Tables used: Meter
# Author: Akshay
# Created on: 13/02/2021

class MeterList(generics.ListAPIView):
    try:
        serializer_class = MeterViewSerializer
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
                    queryset = MeterTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException


# API Header
# API end Point: api/v1/meter
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create meter object
# Usage: API will create meter object based on valid data
# Tables used: Meter
# Author: Akshay
# Created on: 13/02/2021

class Meter(GenericAPIView):
    @is_token_validate
    @role_required(CONSUMER_OPS, METER_DATA, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
        except Exception as ex:
            print('exxx',ex)
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
