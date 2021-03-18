__author__ = "aki"

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from master.models import get_user_by_id_string
from v1.commonapp.views.logger import logger
#from api.constants import CONSUMER_OPS, EDIT, METER_DATA
from v1.meter_data_management.task.assign_revisit_task import assign_revisit_task
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import STATE, ERROR, EXCEPTION, RESULT, SUCCESS
from v1.meter_data_management.models.route_task_assignment import get_route_task_assignment_by_id_string
from v1.meter_data_management.serializers.assign_revisit_task_assignment import \
    AssignRevisitTaskAssignmentViewSerializer

# API Header
# API end Point: api/v1/meter-data/assign-revisit-task-assignment
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create revisit-task-assignment object
# Usage: API will create revisit-task-assignment object based on valid data
# Tables used: RouteTaskAssignment
# Author: Akshay
# Created on: 13/03/2021


class AssignRevisitTaskAssignment(GenericAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, METER_DATA, EDIT)
    def post(self, request):
        try:
            assign_revisit_task_assignment_serializer = AssignRevisitTaskAssignmentViewSerializer(data=request.data)
            if assign_revisit_task_assignment_serializer.is_valid():
                route_task_assignment_obj = get_route_task_assignment_by_id_string(
                    assign_revisit_task_assignment_serializer.validated_data['route_task_assignment_id_staring'])
                user_obj = get_user_by_id_string(
                    assign_revisit_task_assignment_serializer.validated_data['meter_reader_id_string'])
                assign_revisit_task.delay(route_task_assignment_obj.id, user_obj.id,
                                          assign_revisit_task_assignment_serializer.validated_data['meter_no'],
                                          assign_revisit_task_assignment_serializer.validated_data['consumer_no'])
                return Response({
                    STATE: SUCCESS,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: assign_revisit_task_assignment_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
