import traceback
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from api.constants import *
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from v1.work_order.serializers.service_appointment import ServiceAppointmentSerializer,ServiceAppointmentViewSerializer,ServiceAppointmentListSerializer
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from master.models import get_user_by_id_string
from v1.work_order.models.service_appointments import ServiceAppointment as ServiceAppointmentTbl,get_service_appointment_by_id_string,SERVICE_APPOINTMENT_DICT
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django.db import transaction
from v1.work_order.models.service_assignment import get_service_assignment_by_appointment_id
from v1.commonapp.serializers.lifecycle import LifeCycleListSerializer
from v1.commonapp.models.lifecycle import LifeCycle
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.notes import Notes
from django.db.models import Q
from v1.commonapp.views.custom_filter_backend import CustomFilter
from v1.work_order.views.tasks import save_service_appointment_timeline
from v1.work_order.views.common_functions import set_meter_install_data
from v1.work_order.signals.signals import complete_installation_service_appointment,installation_complete_service_appointment, \
    disconnection_complete_service_appointment,complete_disconnection_service_appointment                                       
from v1.commonapp.models.global_lookup import get_global_lookup_by_id, get_global_lookup_by_id_string
from datetime import date, timedelta
from dateutil.parser import parse
# from word2number import w2n

# API Header
# API end Point: api/v1/service-appointment/:id_string/list
# API verb: GET
# Interaction: Service Appointment list
# Usage: API will fetch all Service Appointment List
# Tables used: ServiceAppointment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
# Author: Priyanka
# Created on: 29/12/2020

class ServiceAppointmentList(generics.ListAPIView):
    try:
        serializer_class = ServiceAppointmentListSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('sa_number','sa_name', 'tenant__id_string',)
        ordering_fields = ('sa_number', 'sa_name','tenant',)
        ordering = ('sa_number',)  # always give by default alphabetical order
        search_fields = ('sa_number','sa_name', 'tenant__name',)

        def get_queryset(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.request.query_params['utility_id_string'])
                    queryset = ServiceAppointmentTbl.objects.filter(utility=utility,is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset.reverse()
                    else:
                        raise CustomAPIException("Service Appointment not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer ops', sub_module='Consumer')


# API Header
# API end Point: api/v1/service-appointment
# API verb: POST
# Package: Basic
# Modules: Work Order
# Sub Module: 
# Interaction: Add Work Order
# Usage: Add
# Tables used: ServiceAppointment
# Author: Priyanka
# Created on: 26/12/2020

class ServiceAppointment(GenericAPIView):
    
    @is_token_validate
    #role_required(WORK_ORDER, DISPATCHER, EDIT)
    def post(self, request):
        try:
            appointment_serializer = ServiceAppointmentSerializer(data=request.data)
            if appointment_serializer.is_valid(raise_exception=False):
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                with transaction.atomic():
                    appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                    # Timeline code start                    
                    transaction.on_commit(
                        lambda: save_service_appointment_timeline.delay(appointment_obj, "Service Appointment", "Service Appointment Created", "NOT ASSIGNED",user))
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
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/service-appointment
# API verb: GET, PUT
# Package: Basic
# Modules: User
# Sub Module: Service Appointment
# Interaction: View Service Appointment, Edit Service Appointment
# Usage: View, Edit Service Appointment/ this put api also used for mobile side
# Tables used: ServiceAppointment
# Author: Priyanka
# Created on: 05/01/2021


class ServiceAppointmentDetail(GenericAPIView):
    
    @is_token_validate
    #role_required(WORK_ORDER, DISPATCHER, EDIT)
    def get(self, request, id_string):
        try:
            service_appointment = get_service_appointment_by_id_string(id_string)
            if service_appointment:
                serializer = ServiceAppointmentViewSerializer(instance=service_appointment, context={'request': request})
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

    @is_token_validate
    #role_required(WORK_ORDER, DISPATCHER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            service_appointment = get_service_appointment_by_id_string(id_string)
            if service_appointment:
                service_assignment_obj = get_service_assignment_by_appointment_id(service_appointment.id).last()
                # condition for the disconnection ckeck 
                if 'disconnect_meter' in self.request.query_params:
                    if self.request.query_params['disconnect_meter'] == 'true':
                        service_appointment.save()
                else:
                    serializer = ServiceAppointmentSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        with transaction.atomic():      
                            service_appointment_obj = serializer.update(service_appointment, serializer.validated_data, user)
                            # State change for service assignment start
                            service_appointment_obj.change_state(SERVICE_APPOINTMENT_DICT["COMPLETED"])
                            # State change for service assignment end
                            
                            # Soft Delete entry from Service Assignment start
                            service_assignment_obj.is_active = False
                            service_assignment_obj.save()
                            # Soft Delete entry from Service Assignment end
                            if service_appointment_obj.completed_task_details['key'] == 'New_Meter_Installation':
                                data = set_meter_install_data(service_appointment_obj,'NEW_METER')
                                # Signal for service appointment
                                installation_complete_service_appointment.connect(complete_installation_service_appointment)
                                installation_complete_service_appointment.send(service_appointment_obj,key='NEW_METER', data=data)
                                # Signal for service appointment

                            elif service_appointment_obj.completed_task_details['key'] == 'Existing_Meter_Installation':
                                data = set_meter_install_data(service_appointment_obj,'EXISTING_METER')
                                # Signal for service appointment
                                installation_complete_service_appointment.connect(complete_installation_service_appointment)
                                installation_complete_service_appointment.send(service_appointment_obj,key='EXISTING_METER', data=data)
                                # Signal for service appointment

                            elif service_appointment_obj.completed_task_details['key'] == 'Permanent_Disconnection':
                                disconnection_complete_service_appointment.connect(complete_disconnection_service_appointment)
                                disconnection_complete_service_appointment.send(service_appointment_obj,key='PERMANENT')

                            elif service_appointment_obj.completed_task_details['key'] == 'Temporary_Disconnection':
                                disconnection_complete_service_appointment.connect(complete_disconnection_service_appointment)
                                disconnection_complete_service_appointment.send(service_appointment_obj,key='TEMPORARY')

                        view_serializer = ServiceAppointmentViewSerializer(instance=service_appointment_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: view_serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULT: list(serializer.errors.values())[0][0],
                        }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: SERVICE_APPOINTMENT_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Work Order', Sub_module='service_appointment')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)



# API Header
# API end Point: api/v1/work-order/appointment/:id_string/life-cycles
# API verb: GET
# Package: Basic
# Modules:Work Order
# Sub Module: Dispatcher
# Interaction: Service Appointment lifecycles
# Usage: API will fetch required data for Service Appointment lifecycles
# Tables used: LifeCycles
# Author: Priyanka
# Created on: 11/02/2021
class ServiceAppointmentLifeCycleList(generics.ListAPIView):
    try:
        serializer_class = LifeCycleListSerializer
        pagination_class = StandardResultsSetPagination
        
        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    service_appointment = get_service_appointment_by_id_string(self.kwargs['id_string'])
                    module = get_module_by_key("WX")
                    sub_module = get_sub_module_by_key("DISPATCHER")
                    queryset = LifeCycle.objects.filter(object_id=service_appointment.id, module_id=module, sub_module_id=sub_module, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Lifecycles not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Work Order', sub_module='DISPATCHER')



class ServiceAppointmentReject(GenericAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            service_appointment = get_service_appointment_by_id_string(id_string)
            if service_appointment:
                serializer = ServiceAppointmentSerializer(data=request.data)
                service_appointment.change_state(SERVICE_APPOINTMENT_DICT["REJECTED"])
                if serializer.is_valid(raise_exception=False):
                    service_appointment = serializer.update(service_appointment, serializer.validated_data, user)
                    with transaction.atomic():
                        # State change for payment start                    
                        # State change for payment end
                        serializer = ServiceAppointmentViewSerializer(instance=service_appointment, context={'request': request})
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
            logger().log(e, 'MEDIUM', module='Work Order', Sub_module='service_appointment')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)



class ServiceAppointmentHold(GenericAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            service_appointment = get_service_appointment_by_id_string(id_string)
            if service_appointment:
                serializer = ServiceAppointmentSerializer(data=request.data)
                service_appointment.change_state(SERVICE_APPOINTMENT_DICT["HOLD"])
                if serializer.is_valid(raise_exception=False):
                    service_appointment = serializer.update(service_appointment, serializer.validated_data, user)
                    with transaction.atomic():
                        # State change for payment start                    
                        # State change for payment end
                        serializer = ServiceAppointmentViewSerializer(instance=service_appointment, context={'request': request})
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
            logger().log(e, 'MEDIUM', module='Work Order', Sub_module='service_appointment')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


class ServiceRequestApprove(GenericAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            service_appointment = get_service_appointment_by_id_string(id_string)
            if service_appointment:
                print("request data=====",request.data)
                sd = parse(request.data['start_date'])
                ed = parse(request.data['end_date'])
                # start = sd.strftime('%m/%d/%Y')
                # end = ed.strftime('%m/%d/%Y')
                print("difference === ",(ed - sd).days)
                print("frequency=",get_global_lookup_by_id_string(request.data['frequency_id']))
                print("repeat_every_id=",get_global_lookup_by_id_string(request.data['repeat_every_id']).value)
                print("recurring_id=",get_global_lookup_by_id_string(request.data['recurring_id']).value)
                print("start date=",sd)
                print("end date=",ed)
                recurrence = get_global_lookup_by_id_string(request.data['recurring_id']).value
                frequency_obj = get_global_lookup_by_id_string(request.data['frequency_id'])
                repeat_every = get_global_lookup_by_id_string(request.data['repeat_every_id']).value
                print("type of repeat",type(repeat_every))
                if recurrence == "Yes":
                    print("inside")
                    # repeat_value = w2n.word_to_num(repeat_every)
                    repeat = list(filter(str.isdigit, repeat_every))
                    repeat_value = int(repeat.pop())
                    date_diff = (ed - sd).days
                    r=1
                    # request.data['recurring_id'] = get_global_lookup_by_id(request.data['recurring_id']).id_string
                    # request.data['frequency_id'] = get_global_lookup_by_id(request.data['frequency_id']).id_string
                    # request.data['repeat_every_id'] = get_global_lookup_by_id(request.data['repeat_every_id']).id_string
                    if frequency_obj.key == 'daily':
                        days = repeat_value
                        print("days = ",days)
                        service_number = abs(date_diff/repeat_value)
                        print("days calculate",int(service_number))
                        while r < int(service_number):
                            print("inside service")
                            appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                            print("this ie request data",request.data)
                            if appointment_serializer.is_valid(raise_exception=True):
                                appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                                # appointment_obj.utility = consumer_service_contract_detail_obj.utility
                                appointment_obj.is_active = True
                                appointment_obj.sa_date = sd + timedelta(days=days)
                                appointment_obj.state = 1
                                appointment_obj.save()
                            print("days before",days)
                            days +=repeat_value
                            print("days after",days)
                            r +=1
                        print("rep",service_number)

                    if frequency_obj.key == 'weekly':
                        week=repeat_value * 7
                        week_store = repeat_value * 7
                        print("week calculate",week)
                        service_number = abs(date_diff/week)
                        print("days calculate",int(service_number))
                        while r < int(service_number):
                            print("inside service")
                            appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                            print("this ie request data",request.data)
                            if appointment_serializer.is_valid(raise_exception=True):
                                appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                                # appointment_obj.utility = consumer_service_contract_detail_obj.utility
                                appointment_obj.is_active = True
                                appointment_obj.sa_date = sd + timedelta(days=week)
                                appointment_obj.state = 1
                                appointment_obj.save()
                            week +=week_store
                            r +=1
                        print("rep",service_number)

                    if frequency_obj.key == 'monthly':
                        month=repeat_value * 30
                        month_store=repeat_value * 30
                        print("month calculate",month)
                        service_number = abs(date_diff/month)
                        print("days calculate",int(service_number))
                        while r < int(service_number):
                            print("inside service")
                            appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                            print("this ie request data",request.data)
                            if appointment_serializer.is_valid(raise_exception=True):
                                appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                                # appointment_obj.utility = consumer_service_contract_detail_obj.utility
                                appointment_obj.is_active = True
                                appointment_obj.sa_date = sd + timedelta(days=month)
                                appointment_obj.state = 1
                                appointment_obj.save()
                            month +=month_store
                            r +=1
                        print("rep",service_number)

                    if frequency_obj.key == 'yearly':
                        year=repeat_value * 365
                        year_store=repeat_value * 365
                        print("year calculate",year)
                        service_number = abs(date_diff/year)
                        print("days calculate",int(service_number))
                        while r < int(service_number):
                            print("inside service")
                            appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                            print("this ie request data",request.data)
                            if appointment_serializer.is_valid(raise_exception=True):
                                appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                                # appointment_obj.utility = consumer_service_contract_detail_obj.utility
                                appointment_obj.is_active = True
                                appointment_obj.sa_date = sd + timedelta(days=year)
                                appointment_obj.state = 1
                                appointment_obj.save()
                            year +=year_store
                            r +=1
                        print("rep",service_number)
                serializer = ServiceAppointmentSerializer(data=request.data)
                service_appointment.change_state(SERVICE_APPOINTMENT_DICT["NOT ASSIGNED"])
                service_appointment.is_active=True
                service_appointment.save()
                if serializer.is_valid(raise_exception=False):
                    service_appointment = serializer.update(service_appointment, serializer.validated_data, user)
                    with transaction.atomic():
                        # State change for payment start                    
                        # State change for payment end
                        serializer = ServiceAppointmentViewSerializer(instance=service_appointment, context={'request': request})
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
            print("error  ",e)
            logger().log(e, 'MEDIUM', module='Work Order', Sub_module='service_appointment')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


class ServiceAppointmentApprove(GenericAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, COMPLAINT, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            service_appointment = get_service_appointment_by_id_string(id_string)
            if service_appointment:
                serializer = ServiceAppointmentSerializer(data=request.data)
                service_appointment.change_state(SERVICE_APPOINTMENT_DICT["NOT ASSIGNED"])
                service_appointment.is_active=True
                service_appointment.save()
                if serializer.is_valid(raise_exception=False):
                    service_appointment = serializer.update(service_appointment, serializer.validated_data, user)
                    with transaction.atomic():
                        # State change for payment start                    
                        # State change for payment end
                        serializer = ServiceAppointmentViewSerializer(instance=service_appointment, context={'request': request})
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
            logger().log(e, 'MEDIUM', module='Work Order', Sub_module='service_appointment')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


