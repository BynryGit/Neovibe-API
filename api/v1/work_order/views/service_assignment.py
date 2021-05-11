import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.db import transaction
from api.messages import *
from api.constants import *
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from v1.work_order.serializers.service_assignment import ServiceAssignmentSerializer,ServiceAssignmentViewSerializer
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from master.models import get_user_by_id_string
from v1.work_order.models.service_appointments import get_service_appointment_by_id_string, SERVICE_APPOINTMENT_DICT
from v1.work_order.models.service_assignment import get_service_assignment_by_appointment_id, SERVICE_ASSIGNMENT_DICT, get_service_assignment_by_id_string
from v1.work_order.serializers.service_assignment import ServiceAssignmentListSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.work_order.models.service_assignment import ServiceAssignment as ServiceAssignmentTbl
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.work_order.views.tasks import save_service_appointment_timeline


# API Header
# API end Point: api/v1/utility/:id_string/user/:id_string/service-assignment/list
# API verb: GET
# Interaction: Service Assignment list
# Usage: API will fetch all Service Assignment List & send data to mobile side
# Tables used: ServiceAssignment
# Author: Priyanka
# Created on: 01/02/2020

class ServiceAssignmentList(generics.ListAPIView):
    try:
        serializer_class = ServiceAssignmentListSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('user_id','sa_id', 'tenant__id_string',)
        ordering_fields = ('user_id', 'sa_id','tenant',)
        ordering = ('user_id',)  # always give by default alphabetical order
        search_fields = ('user_id','sa_id', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['utility_id_string'])
                    user = get_user_by_id_string(self.kwargs['user_id_string'])
                    if user:
                        queryset = ServiceAssignmentTbl.objects.filter(utility=utility,user_id=user.id,is_active=True)
                        if queryset:
                            return queryset
                        else:
                            raise CustomAPIException("Service Appointment not found.", status.HTTP_404_NOT_FOUND)
                    else:
                        raise CustomAPIException("User not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer ops', sub_module='Consumer')


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
    #role_required(WORK_ORDER, DISPATCHER, EDIT)
    def post(self, request):
        try:
            print('======',request.data)
            assignment_serializer = ServiceAssignmentSerializer(data=request.data)
            if assignment_serializer.is_valid(raise_exception=True):
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                service_appoint_obj = get_service_appointment_by_id_string(request.data['sa_id'])
                with transaction.atomic():                    
                    assignment_obj = assignment_serializer.create(assignment_serializer.validated_data, user)

                    # State change for service assignment start
                    assignment_obj.change_state(SERVICE_ASSIGNMENT_DICT["ASSIGNED"])
                    # State change for service assignment end

                    

                    # State change for service appointment start
                    service_appoint_obj.change_state(SERVICE_APPOINTMENT_DICT["ASSIGNED"])
                    # State change for service appointment end

                    # Timeline code start
                    transaction.on_commit(
                        lambda: save_service_appointment_timeline.delay(service_appoint_obj, "Service Appointment", "Service Appointment Assigned", "ASSIGNED",user))
                    # Timeline code end

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

    


# API Header
# API end Point: api/v1/work_order/service-dessignment/:id_string
# API verb:  PUT
# Package: Basic
# Modules: Work Order
# Sub Module: Dispatch
# Interaction:  Update Assignment
# Usage: Update
# Tables used: ServiceAssignment
# Auther: Priyanka
# Created on: 13/01/2021

class ServiceDessignmentDetail(GenericAPIView):

    @is_token_validate
    #role_required(WORK_ORDER, DISPATCHER, EDIT)
    def put(self, request, id_string):
        try:
            deassignment_serializer = ServiceAssignmentSerializer(data=request.data)
            if deassignment_serializer.is_valid(raise_exception=True):
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                appointmentObj = get_service_appointment_by_id_string(id_string)
                if appointmentObj:
                    assignmentObj = get_service_assignment_by_appointment_id(appointmentObj.id).first()
                    if assignmentObj:
                        with transaction.atomic():   
                            dessignment_obj = deassignment_serializer.update(assignmentObj, deassignment_serializer.validated_data, user)

                            # State change for service appointment start
                            appointmentObj.change_state(SERVICE_APPOINTMENT_DICT["NOT ASSIGNED"])
                            # State change for service appointment end

                            # Timeline code start
                            transaction.on_commit(
                                lambda: save_service_appointment_timeline.delay(appointmentObj, "Service Appointment", "Service Appointment Deassign", "DEASSIGN",user))
                            # Timeline code end

                            return Response({
                                STATE: SUCCESS,
                                RESULTS: SERVICE_DEASSIGNMENT,
                            }, status=status.HTTP_201_CREATED) 
                    else:
                        return Response({
                        STATE: ERROR,
                        RESULTS: SERVICE_ASSIGNMENT_NOT_FOUND,
                    }, status=status.HTTP_400_BAD_REQUEST) 
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_400_BAD_REQUEST)              
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(deassignment_serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

class ServiceAssignmentDetail(GenericAPIView):
    
    @is_token_validate
    #role_required(WORK_ORDER, DISPATCHER, EDIT)
    def get(self, request, id_string):
        try:
            service_appointment = get_service_appointment_by_id_string(id_string)
            service_assignment = get_service_assignment_by_appointment_id(service_appointment.id).first()
            if service_assignment:
                serializer = ServiceAssignmentViewSerializer(instance=service_assignment, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    RESULTS: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


