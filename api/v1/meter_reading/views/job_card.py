__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.meter_reading.serializers.job_card import JobcardViewSerializer
from v1.meter_reading.models.jobcard import Jobcard as JobcardTbl


# API Header
# API end Point: api/v1/meter-data/job-card/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: job card list
# Usage: API will fetch required data for job card list against filter and search
# Tables used: 2.3.8.3 Jobcard
# Author: Akshay
# Created on: 16/06/2020


class JobcardList(generics.ListAPIView):
    try:
        serializer_class = JobcardViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('consumer_no',)
        ordering_fields = ('consumer_no',)
        ordering = ('consumer_no',) # always give by default alphabetical order
        search_fields = ('consumer_no',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = JobcardTbl.objects.filter(meter_reader_id=1, is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException