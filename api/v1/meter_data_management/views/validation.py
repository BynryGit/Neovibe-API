__author__ = "aki"

from django.db.models import Q
from rest_framework.exceptions import APIException
from rest_framework import generics
from master.models import get_user_by_id_string
from v1.commonapp.views.logger import logger
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id_string
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id_string
from v1.meter_data_management.serializers.validation import ValidationViewSerializer
from v1.userapp.models.role import Role as RoleTbl
from v1.userapp.models.user_role import UserRole as UserRoleTbl


# API Header
# API end Point: api/v1/meter-data/validation-one/schedule-log/<uuid:schedule_log>/read-cycle/<uuid:read_cycle>/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter reading list
# Usage: API will fetch required data for meter reading list against filter and search
# Tables used: Meter Reading
# Author: Akshay
# Created on: 16/03/2021


class ValidationList(generics.ListAPIView):
    try:
        serializer_class = ValidationViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string',)
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name', 'consumer_no', 'meter_no')

        def get_serializer_context(self):
            """
            Extra context provided to the serializer class.
            """
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            return {
                'user_id_string': user_obj,
                'schedule_log_id_string': self.kwargs['schedule_log'],
                'read_cycle_id_string': self.kwargs['read_cycle'],
            }

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    user_obj = get_user_by_id_string(user_obj)
                    user_role_obj = UserRoleTbl.objects.get(user_id=user_obj.id)
                    role_obj = RoleTbl.objects.get(id=user_role_obj.role_id)
                    schedule_log_obj = get_schedule_log_by_id_string(self.kwargs['schedule_log'])
                    read_cycle_obj = get_read_cycle_by_id_string(self.kwargs['read_cycle'])
                    if role_obj.role_ID == 'Validator_One':
                        queryset = MeterReadingTbl.objects.filter((Q(reading_status=0) | Q(reading_status=2)),
                                                                  validator_one_id=user_obj.id,
                                                                  read_cycle_id=read_cycle_obj.id,
                                                                  schedule_log_id=schedule_log_obj.id,
                                                                  is_active=True, is_duplicate=False)
                        return queryset
                    elif role_obj.role_ID == 'Validator_Two':
                        queryset = MeterReadingTbl.objects.filter((Q(reading_status=1) | Q(reading_status=2)),
                                                                  validator_two_id=user_obj.id,
                                                                  read_cycle_id=read_cycle_obj.id,
                                                                  schedule_log_id=schedule_log_obj.id,
                                                                  is_active=True, is_duplicate=False)
                        return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException
