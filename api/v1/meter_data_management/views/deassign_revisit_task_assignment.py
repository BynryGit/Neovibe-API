__author__ = "aki"

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from v1.commonapp.views.logger import logger
from api.constants import MX, EDIT, DISPATCH
from v1.meter_data_management.task.de_assign_revisit_task import de_assign_revisit_task
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import STATE, ERROR, EXCEPTION, RESULT, SUCCESS
from v1.meter_data_management.models.route_task_assignment import get_route_task_assignment_by_id_string
from v1.meter_data_management.serializers.deassign_revisit_task_assignment import \
    DeAssignRevisitTaskAssignmentViewSerializer

# API Header
# API end Point: api/v1/meter-data/de-assign-revisit-task-assignment
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create revisit-task-assignment object
# Usage: API will create revisit-task-assignment object based on valid data
# Tables used: RouteTaskAssignment
# Author: Akshay
# Created on: 13/03/2021


class DeAssignRevisitTaskAssignment(GenericAPIView):
    @is_token_validate
    # @role_required(MX, DISPATCH, EDIT)
    def post(self, request):
        try:
            de_assign_revisit_task_assignment_serializer = DeAssignRevisitTaskAssignmentViewSerializer(data=request.data)
            if de_assign_revisit_task_assignment_serializer.is_valid():
                route_task_assignment_obj = get_route_task_assignment_by_id_string(
                    de_assign_revisit_task_assignment_serializer.validated_data['route_task_assignment_id_staring'])
                de_assign_revisit_task.delay(route_task_assignment_obj.id,
                                             de_assign_revisit_task_assignment_serializer.validated_data['meter_no'],
                                             de_assign_revisit_task_assignment_serializer.validated_data['consumer_no'])
                return Response({
                    STATE: SUCCESS,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: de_assign_revisit_task_assignment_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='DISPATCH')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
