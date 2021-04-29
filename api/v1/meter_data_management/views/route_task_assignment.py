__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.constants import MX, EDIT, DISPATCH, VIEW
from master.models import get_user_by_id_string
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, ROUTE_TASK_ASSIGNMENT_NOT_FOUND
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment as RouteTaskAssignmentTbl, \
    get_route_task_assignment_by_id_string
from v1.meter_data_management.serializers.route_task_assignment import RouteTaskAssignmentViewSerializer, \
    RouteTaskAssignmentSerializer
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException, \
    AllocationInProgress, ObjectNotFoundException


# API Header
# API end Point: api/v1/meter-data/route-task-assignment/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: route task assignment list
# Usage: API will fetch required data for route task assignment list against filter and search
# Tables used: Route Task Assignment
# Author: Akshay
# Created on: 09/03/2021


class RouteTaskAssignmentList(generics.ListAPIView):
    try:
        serializer_class = RouteTaskAssignmentViewSerializer
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
                    user = get_user_by_id_string(user_obj)
                    route_task_assignment_obj = RouteTaskAssignmentTbl.objects.filter(meter_reader_id=user.id,
                                                                                      state=1, is_active=True)
                    if route_task_assignment_obj.exists():
                        raise AllocationInProgress
                    else:
                        route_task_assignment_obj = RouteTaskAssignmentTbl.objects.filter(meter_reader_id=user.id,
                                                                                          consumer_meter_json__contains=
                                                                                          [{'is_active': True},
                                                                                           {'status': 'ALLOCATED'}],
                                                                                          is_active=True)
                        if route_task_assignment_obj.exists():
                            return route_task_assignment_obj
                        else:
                            raise ObjectNotFoundException
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='MX', sub_module='DISPATCH')
        raise APIException


# API Header
# API end Point: api/v1/meter-data/route-task-assignment
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create route-task-assignment object
# Usage: API will create route-task-assignment object based on valid data
# Tables used: RouteTaskAssignment
# Author: Akshay
# Created on: 03/03/2021

class RouteTaskAssignment(GenericAPIView):
    @is_token_validate
    # @role_required(MX, DISPATCH, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            route_task_assignment_serializer = RouteTaskAssignmentSerializer(data=request.data)
            if route_task_assignment_serializer.is_valid():
                route_task_assignment_obj = route_task_assignment_serializer.create\
                    (route_task_assignment_serializer.validated_data, user)
                return Response({
                    STATE: SUCCESS,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: route_task_assignment_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='DISPATCH')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/meter-data/route-task-assignment/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View route-task-assignment object
# Usage: API will fetch and edit required data for route task assignment using id_string
# Tables used: RouteTaskAssignment
# Author: Akshay
# Created on: 27/02/2021

class RouteTaskAssignmentDetail(GenericAPIView):
    @is_token_validate
    # @role_required(MX, DISPATCH, VIEW)
    def get(self, request, id_string):
        try:
            route_task_assignment_obj = get_route_task_assignment_by_id_string(id_string)
            if route_task_assignment_obj:
                route_task_assignment_serializer = RouteTaskAssignmentViewSerializer(instance=route_task_assignment_obj,
                                                                                     context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: route_task_assignment_serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: ROUTE_TASK_ASSIGNMENT_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='DISPATCH')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    # @role_required(MX, DISPATCH, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            route_task_assignment_obj = get_route_task_assignment_by_id_string(id_string)
            if route_task_assignment_obj:
                route_task_assignment_serializer = RouteTaskAssignmentSerializer(data=request.data)
                if route_task_assignment_serializer.is_valid():
                    route_task_assignment_obj = route_task_assignment_serializer.update(route_task_assignment_obj,
                                                                                        route_task_assignment_serializer.
                                                                                        validated_data, user)
                    route_task_assignment_view_serializer = RouteTaskAssignmentViewSerializer\
                        (instance=route_task_assignment_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: route_task_assignment_view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: route_task_assignment_obj.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: ROUTE_TASK_ASSIGNMENT_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='DISPATCH')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
