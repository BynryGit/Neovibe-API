import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from api.constants import *
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from v1.work_order.serializers.service_assignment import ServiceAssignmentSerializer,ServiceAssignmentViewSerializer
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from master.models import get_user_by_id_string

# API Header
# API end Point: api/v1/service-assignment
# API verb: POST
# Package: Basic
# Modules: Work Order
# Sub Module: 
# Interaction: Add Service Assignment
# Usage: Add
# Tables used: ServiceAssignment
# Author: Priyanka
# Created on: 12/01/2021

class ServiceAssignment(GenericAPIView):
    
    @is_token_validate
    @role_required(WORK_ORDER, DISPATCHER, EDIT)
    def post(self, request):
        try:
            assignment_serializer = ServiceAssignmentSerializer(data=request.data)
            if assignment_serializer.is_valid(raise_exception=True):
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                assignment_obj = assignment_serializer.create(assignment_serializer.validated_data, user)
                view_serializer = ServiceAssignmentViewSerializer(instance=assignment_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)                
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(assignment_serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)
