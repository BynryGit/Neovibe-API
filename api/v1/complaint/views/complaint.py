from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.constants import *
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import get_consumer_complaint_by_id_string, COMPLAINT_DICT,Complaint as ComplaintTbl
from v1.complaint.models.complaint_assignment import get_complaint_assignments_by_field_operator_id
from v1.complaint.serializers.complaint import ComplaintViewSerializer,ComplaintListSerializer, ComplaintSerializer
from v1.complaint.serializers.complaint_assignment import ComplaintAssignmentListSerializer
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from v1.commonapp.views.custom_filter_backend import CustomFilter
from v1.work_order.serializers.service_appointment import ServiceAppointmentSerializer,ServiceAppointmentViewSerializer,ServiceAppointmentListSerializer

# API Header
# API end Point: api/v1/complaint/assignment/list
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Complaint
# Interaction: Complaint assignmet list
# Usage: API will fetch required data for Complaint assignment list
# Tables used: CompaintAssignment, Complaint, User
# Author: Rohan
# Created on: 13/07/2020
class ComplaintAssignmentList(generics.ListAPIView):
    try:
        serializer_class = ComplaintAssignmentListSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('created_date',)
        ordering_fields = ('created_date',)
        ordering = ('created_date',)
        search_fields = ('created_date',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized(1, 1, 1, 1):
                    user_id_string = get_user_from_token(self.request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    if user:
                        queryset = get_complaint_assignments_by_field_operator_id(user.id)
                        return queryset
                    else:
                        raise InvalidAuthorizationException
                else:
                    raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/complaint/:id_string
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Complaint
# Interaction: Complaint
# Usage: API will get complaint detail.
# Tables used: Complaint, User
# Author: Rohan
# Created on: 14/07/2020
class ComplaintDetail(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, VIEW)
    def get(self, request, id_string):
        try:
            complaint = get_consumer_complaint_by_id_string(id_string)
            if complaint:
                serializer = ComplaintViewSerializer(instance=complaint, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: COMPLAINT_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Consumer Ops', Sub_module='Complaint')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            complaint_obj = get_consumer_complaint_by_id_string(id_string)
            if complaint_obj:
                serializer = ComplaintSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    complaint_obj = serializer.update(complaint_obj, serializer.validated_data, user)
                    view_serializer = ComplaintViewSerializer(instance=complaint_obj,
                                                          context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

# API Header
# API end Point: api/v1/complaint/:id_string/accept
# API verb: PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Complaint
# Interaction: Complaint
# Usage: API will change the state of complaint to accept
# Tables used: CompaintAssignment, Complaint, User
# Author: Rohan
# Created on: 14/07/2020
class ComplaintAccept(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            complaint = get_consumer_complaint_by_id_string(id_string)
            if complaint:
                with transaction.atomic():
                    # State change for payment start
                    complaint.change_state(COMPLAINT_DICT["ACCEPTED"])
                    # State change for payment end
                serializer = ComplaintViewSerializer(instance=complaint, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: COMPLAINT_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Complaint')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/complaint/:id_string/reject
# API verb: PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Complaint
# Interaction: Complaint
# Usage: API will change the state of complaint to reject
# Tables used: CompaintAssignment, Complaint, User
# Author: Rohan
# Created on: 14/07/2020
class ComplaintReject(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            complaint = get_consumer_complaint_by_id_string(id_string)
            if complaint:
                serializer = ComplaintSerializer(data=request.data)
                complaint.change_state(COMPLAINT_DICT["REJECTED"])
                if serializer.is_valid(raise_exception=False):
                    complaint = serializer.update(complaint, serializer.validated_data, user)
                    with transaction.atomic():
                        # State change for payment start                    
                        # State change for payment end
                        serializer = ComplaintViewSerializer(instance=complaint, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: COMPLAINT_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Complaint')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/complaint/:id_string/hold
# API verb: PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Complaint
# Interaction: Complaint
# Usage: API will change the state of complaint to reject
# Tables used: CompaintAssignment, Complaint, User
# Author: Gauarv
# Created on: 27/03/2021

class ComplaintHold(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            complaint = get_consumer_complaint_by_id_string(id_string)
            if complaint:
                serializer = ComplaintSerializer(data=request.data)
                complaint.change_state(COMPLAINT_DICT["HOLD"])
                if serializer.is_valid(raise_exception=False):
                    complaint = serializer.update(complaint, serializer.validated_data, user)
                    with transaction.atomic():
                        # State change for payment start                    
                        # State change for payment end
                        serializer = ComplaintViewSerializer(instance=complaint, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: COMPLAINT_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Complaint')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/complaint/:id_string/comlete
# API verb: PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Complaint
# Interaction: Complaint
# Usage: API will change the state of complaint to complete
# Tables used: CompaintAssignment, Complaint, User
# Author: Rohan
# Created on: 14/07/2020
class ComplaintComplete(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            complaint = get_consumer_complaint_by_id_string(id_string)
            if complaint:
                with transaction.atomic():
                    # State change for payment start
                    complaint.change_state(COMPLAINT_DICT["COMPLETED"])
                    # State change for payment end
                serializer = ComplaintViewSerializer(instance=complaint, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: COMPLAINT_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Complaint')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/complaint/utility/:id_string/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Complaint list
# Usage: API will fetch all Complaints list
# Tables used: Complaint
# Author: Chinmay
# Created on: 4/12/2020

class ComplaintList(generics.ListAPIView):
    try:
        serializer_class = ComplaintListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('complaint_name', 'tenant__id_string',)
        ordering_fields = ('complaint_name', 'tenant',)
        ordering = ('complaint_name',)  # always give by default alphabetical order
        search_fields = ('complaint_name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ComplaintTbl.objects.filter(utility=utility, is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Complaint not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')



# API Header
# API end Point: api/v1/complaint/:id_string/approve
# API verb: POST
# Package: Basic
# Modules: Work Order
# Sub Module: 
# Interaction: Add Work Order
# Usage: Add
# Tables used: ServiceAppointment
# Author: Gaurav
# Created on: 25/03/2021

class ComplaintApprove(GenericAPIView):
    
    @is_token_validate
    #role_required(WORK_ORDER, DISPATCHER, EDIT)
    def post(self, request, id_string):
        try:
            complaint = get_consumer_complaint_by_id_string(id_string)
            remark=request.data['sa_user_remark']
            appointment_serializer = ServiceAppointmentSerializer(data=request.data)
            if appointment_serializer.is_valid(raise_exception=False):
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                with transaction.atomic():
                    complaint.change_state(COMPLAINT_DICT["IN PROGRESS"])
                    complaint.closure_remark=remark
                    complaint.save()
                    appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                    # # Timeline code start
                    # transaction.on_commit(
                    #     lambda: save_service_appointment_timeline.delay(appointment_obj, "Service Appointment", "Service Appointment Created", "NOT ASSIGNED",user))
                        # Timeline code end
                    view_serializer = ServiceAppointmentViewSerializer(instance=appointment_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_201_CREATED)                
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(appointment_serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("=======error=========",e)
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)