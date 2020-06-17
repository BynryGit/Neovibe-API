__author__ = "aki"

import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DUPLICATE, RESULT, DATA_ALREADY_EXISTS
from master.models import User
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.meter_reading.models.route import get_route_by_id_string
from v1.meter_reading.models.route_assignment import get_route_assignment_by_id
from v1.meter_reading.serializers.route_assignment import RouteAssignmentSerializer, RouteAssignmentViewSerializer, \
    RouteDeAssignmentSerializer
from v1.meter_reading.task.create_job_card import create_job_card, update_job_card


# API Header
# API end Point: api/v1/meter-data/route/id_string/assign
# API verb: POST
# Package: Basic
# Modules: Meter Data
# Sub Module:
# Interaction: Create job card according route
# Usage: API will create job card object based on valid data
# Tables used: RouteAssignment
# Author: Akshay
# Created on: 16/06/2020


class RouteAssignment(GenericAPIView):
    serializer_class = RouteAssignmentSerializer

    def post(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end
                    route_obj = get_route_by_id_string(id_string)
                    if route_obj:
                        serializer = RouteAssignmentSerializer(data=request.data)
                        if serializer.is_valid():
                            route_assignment_obj = serializer.create(serializer.validated_data, route_obj, user)
                            create_job_card.delay(route_assignment_obj.id, route_assignment_obj.month)
                            if route_assignment_obj:
                                serializer = RouteAssignmentViewSerializer(route_assignment_obj, context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULT: serializer.data,
                                }, status=status.HTTP_201_CREATED)
                            else:
                                return Response({
                                    STATE: DUPLICATE,
                                    RESULT: DATA_ALREADY_EXISTS,
                                }, status=status.HTTP_409_CONFLICT)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULT: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
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


# API Header
# API end Point: api/v1/meter-data/route/id_string/deassign
# API verb: POST
# Package: Basic
# Modules: Meter Data
# Sub Module:
# Interaction: Edit job card according route
# Usage: API will edit job card object based on valid data
# Tables used: RouteAssignment
# Author: Akshay
# Created on: 16/06/2020

class RouteAssignmentDetail(GenericAPIView):
    serializer_class = RouteAssignmentSerializer

    def put(self, request, route, route_assignment):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    route_obj = get_route_by_id_string(route)
                    if route_obj:
                        route_assignment_obj= get_route_assignment_by_id(route_assignment)
                        if route_assignment:
                            serializer = RouteDeAssignmentSerializer(data=request.data)
                            if serializer.is_valid():
                                route_assignment_obj = serializer.update(route_assignment_obj, serializer.validated_data, user)
                                update_job_card.delay(route_assignment_obj.id, route_assignment_obj.month)
                                serializer = RouteAssignmentViewSerializer(route_assignment_obj, context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULT: serializer.data,
                                }, status=status.HTTP_200_OK)
                            else:
                                return Response({
                                    STATE: ERROR,
                                    RESULT: serializer.errors,
                                }, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({
                                STATE: ERROR,
                            }, status=status.HTTP_404_NOT_FOUND)
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