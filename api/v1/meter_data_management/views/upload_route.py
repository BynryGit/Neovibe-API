__author__ = "aki"

from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from master.models import get_user_by_id_string
from api.constants import MX, UPLOAD, EDIT
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl
from v1.meter_data_management.serializers.upload_route import UploadRouteViewSerializer, UploadRouteSerializer
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException

# API Header
# API end Point: api/v1/meter-data/upload-route/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: route task assignment list
# Usage: API will fetch required data for route task assignment list against filter and search
# Tables used: Route Task Assignment
# Author: Akshay
# Created on: 23/03/2021


class UploadRouteList(generics.ListAPIView):
    try:
        serializer_class = UploadRouteViewSerializer
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
                    route_task_assignment_obj = RouteTaskAssignmentTbl.objects.filter(is_active=True)
                    return route_task_assignment_obj
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='MX', sub_module='UPLOAD')
        raise APIException


# API Header
# API end Point: api/v1/meter-data/upload-route
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create upload route object
# Usage: API will create upload route object based on valid data
# Tables used: Upload Route
# Author: Akshay
# Created on: 24/03/2021

class UploadRoute(GenericAPIView):
    @is_token_validate
    # @role_required(MX, UPLOAD, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            upload_route_serializer = UploadRouteSerializer(data=request.data)
            if upload_route_serializer.is_valid():
                upload_route_obj = upload_route_serializer.create(upload_route_serializer.validated_data, user)
                if upload_route_obj:
                    return Response({
                        STATE: SUCCESS,
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: upload_route_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='UPLOAD')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
