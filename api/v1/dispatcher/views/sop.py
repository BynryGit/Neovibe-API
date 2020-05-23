from v1.dispatcher.serializers.sop import SOPViewSerializer
from v1.dispatcher.models.sop_master import SopMaster
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
from v1.dispatcher.models.sop_master import get_sop_by_id_string


# API Header
# API end Point: api/v1/asset/sop/list
# API verb: GET
# Package: Basic
# Modules: O&M
# Sub Module:
# Interaction: Sop List
# Usage: API will fetch required data for Sop list
# Tables used:  Sop Master
# Author: Priyanka Kachare
# Created on: 23/05/2020

# Api for getting Sop  filter

class SOPList(generics.ListAPIView):
    try:
        serializer_class = SOPViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string','service_type_id',)
        ordering_fields = ('name',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            if is_token_valid(0):
                if is_authorized():
                    queryset = SopMaster.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/asset/sop/:id_string
# API verb: GET
# Package: Basic
# Modules: O&M
# Sub Module: Asset
# Interaction: View SOP
# Usage: View
# Tables used: SOP Master
# Auther: Priyanka
# Created on: 23/05/2020

# API for view SOP details
class SOPDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    sop_obj = get_sop_by_id_string(id_string)
                    if sop_obj:
                        serializer = SOPViewSerializer(instance=sop_obj, context={'request': request})
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

