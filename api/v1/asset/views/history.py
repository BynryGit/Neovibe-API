__author__ = "Priyanka"

import traceback
import logging
from datetime import datetime
from django.db import transaction
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS,DUPLICATE,DATA_ALREADY_EXISTS
from v1.userapp.models.user_master import UserDetail
from v1.dispatcher.serializers.service_request import ServiceRequestViewSerializer
from v1.dispatcher.models.service_appointments import ServiceRequest
from v1.asset.models.asset_master import get_asset_by_id_string
from v1.dispatcher.models.service_appointments import get_service_request_by_id_string
from v1.dispatcher.serializers.service_request import ServiceRequestViewSerializer

# API Header
# API end Point: api/v1/asset/:id_string/history/list
# API verb: GET
# Package: Basic
# Modules: o&M
# Sub Module:
# Interaction: Asset History List
# Usage: API will fetch required data for Asset History list
# Tables used:  ServiceAssignment
# Author: Priyanka Kachare
# Created on: 26/05/2020

# Api for getting Asset  History list

class ServiceHistoryList(generics.ListAPIView):
    try:
        serializer_class = ServiceRequestViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string','service_name','service_no')
        ordering_fields = ('service_name','service_no')
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('service_name','service_no')

        def get_queryset(self):
            if is_token_valid(0):
                if is_authorized():
                    queryset = ''
                    asset_id = get_asset_by_id_string(self.kwargs['id_string'])
                    if asset_id:
                        queryset = ServiceRequest.objects.filter(asset_id=asset_id.id,is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/asset/history/:Id-string
# API verb: GET
# Package: Basic
# Modules: O&M
# Sub Module:
# Interaction: View History
# Usage: View
# Tables used:  ServiceAssignment
# Auther: Priyanka
# Created on: 26/05/2020

# API for  view History details
class ServiceHistoryDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    service_request = get_service_request_by_id_string(id_string)
                    if service_request:
                        serializer = ServiceRequestViewSerializer(instance=service_request, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

