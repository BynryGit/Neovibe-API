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
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.work_order.serializers.scheduled_appointment import ScheduledAppointmentSerializer, ScheduledAppointmentViewSerializer
from master.models import get_user_by_id_string,get_user_by_id
from datetime import date, datetime
from v1.work_order.models.scheduled_appointment import ScheduledAppointment as ScheduledAppointmentTbl
from v1.work_order.models.service_appointments import get_service_appointment_by_id_string
from v1.work_order.serializers.service_assignment import ServiceAssignmentSerializer,ServiceAssignmentViewSerializer
from v1.work_order.models.service_assignment import get_service_assignment_by_appointment_id, SERVICE_ASSIGNMENT_DICT, get_service_assignment_by_id_string
from v1.work_order.models.service_appointments import get_service_appointment_by_id_string, SERVICE_APPOINTMENT_DICT
from django.db import transaction

# API Header
# API end Point: api/v1/schedule-appointment
# API verb: POST
# Package: Basic
# Modules: Work Order
# Sub Module: 
# Interaction: Add Schedule Appointment
# Usage: Add
# Tables used: ScheduledAppointment
# Author: Priyanka
# Created on: 09/02/2021

class ScheduledAppointment(GenericAPIView):
    
    @is_token_validate
    @role_required(WORK_ORDER, DISPATCHER, EDIT)
    def post(self, request):
        try:
            schedule_appointment_serializer = ScheduledAppointmentSerializer(data=request.data)
            if schedule_appointment_serializer.is_valid(raise_exception=True):
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                appointment_obj = schedule_appointment_serializer.create(schedule_appointment_serializer.validated_data, user)
                view_serializer = ScheduledAppointmentViewSerializer(instance=appointment_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)                
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(schedule_appointment_serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)



def schedule_appointment_assign(request):
    try:
        schedule_objs = ScheduledAppointmentTbl.objects.filter(assignment_date__date = date.today(),is_active=True)
        if schedule_objs:
            data = {}
            for schedule_obj in schedule_objs:
                for appointments in schedule_obj.appointments:
                    service_appoint_obj = get_service_appointment_by_id_string(appointments)
                    data['utility_id'] = str(schedule_obj.utility.id_string)
                    data['sa_id'] = str(service_appoint_obj.id_string)
                    data['user_id'] = str(get_user_by_id(schedule_obj.user_id).id_string)
                    data['assignment_date'] = str(schedule_obj.assignment_date)
                    data['assignment_time'] = str(datetime.now().time())
                    assignment_serializer = ServiceAssignmentSerializer(data=data)
                    user = get_user_by_id(schedule_obj.created_by)
                    if assignment_serializer.is_valid(raise_exception=True):
                        with transaction.atomic():                    
                            assignment_obj = assignment_serializer.create(assignment_serializer.validated_data, user)
                            
                            print('******assignment_obj*',assignment_obj)
                            # State change for service assignment start
                            assignment_obj.change_state(SERVICE_ASSIGNMENT_DICT["ASSIGNED"])
                            # State change for service assignment end

                            # State change for service appointment start
                            service_appoint_obj.change_state(SERVICE_APPOINTMENT_DICT["ASSIGNED"])
                            # State change for service appointment end             
        else:
            pass       
        
    except Exception as e:        
        return Response({
            STATE: EXCEPTION,
            RESULT: str(e),
        }, status=res.status_code)

