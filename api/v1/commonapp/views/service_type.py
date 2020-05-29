__author__ = "Priyank"

from v1.commonapp.serializers.service_type import ServiceTypeListSerializer,ServiceTypeViewSerializer
from v1.commonapp.models.service_type import ServiceType
from v1.commonapp.common_functions import is_token_valid,  is_authorized
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS,DUPLICATE,DATA_ALREADY_EXISTS
import traceback
import logging
from rest_framework.response import Response
from v1.commonapp.views.logger import logger
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.pagination import StandardResultsSetPagination
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from v1.commonapp.models.service_type import get_service_type_by_id_string


# API Header
# API end Point: api/v1/service_type/list
# API verb: GET
# Package: Basic
# Modules: O&M
# Sub Module:
# Interaction: service_type List
# Usage: API will fetch required data for service_type list
# Tables used:  Service Type
# Author: Priyanka Kachare
# Created on: 25/05/2020

# Api for getting Service Type  filter

class ServiceTypeList(generics.ListAPIView):
    try:
        serializer_class = ServiceTypeListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'utility__id_string',)
        ordering_fields = ('name',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            if is_token_valid(0):
                if is_authorized():
                    queryset = ServiceType.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/service_type/:id_string
# API verb: GET
# Package: Basic
# Modules: O&M
# Sub Module:
# Interaction: View service_type
# Usage: View
# Tables used: Service Type
# Auther: Priyanka
# Created on: 25/05/2020

# API for view service_type details
class ServiceTypeDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    service_type_obj = get_service_type_by_id_string(id_string)
                    if service_type_obj:
                        serializer = ServiceTypeViewSerializer(instance=service_type_obj, context={'request': request})
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

