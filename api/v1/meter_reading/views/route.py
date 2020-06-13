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
from v1.meter_reading.serializers.route import RouteViewSerializer
from v1.meter_reading.models.route import Route as RouteTbl, get_route_by_id_string


# API Header
# API end Point: api/v1/meter-data/route/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: route list
# Usage: API will fetch required data for route list against filter and search
# Tables used: 2.12.50 Route Details
# Author: Akshay
# Created on: 12/06/2020

class RouteList(generics.ListAPIView):
    try:
        serializer_class = RouteViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'utility__id_string',)
        ordering_fields = ('name', 'utility__id_string',)
        ordering = ('name',) # always give by default alphabetical order
        search_fields = ('name', 'utility__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = RouteTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/route/id_string
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View route object
# Usage: API will fetch required data for route using id_string
# Tables used: 2.12.50 Route Details
# Author: Akshay
# Created on: 12/06/2020

class RouteDetail(GenericAPIView):
    serializer_class = RouteViewSerializer

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

                    route_obj = get_route_by_id_string(id_string)
                    if route_obj:
                        serializer = RouteViewSerializer(instance=route_obj, context={'request': request})
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
