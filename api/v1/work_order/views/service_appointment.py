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
from v1.work_order.serializers.service_appointment import ServiceAppointmentSerializer,ServiceAppointmentViewSerializer,ServiceAppointmentListSerializer
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from master.models import get_user_by_id_string
from v1.work_order.models.service_appointments import ServiceAppointment as ServiceAppointmentTbl
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination


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
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ServiceAppointmentTbl.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumers not found.", status.HTTP_404_NOT_FOUND)
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
    @role_required(WORK_ORDER, DISPATCHER, EDIT)
    def post(self, request):
        try:
            appointment_serializer = ServiceAppointmentSerializer(data=request.data)
            if appointment_serializer.is_valid(raise_exception=False):
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
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
