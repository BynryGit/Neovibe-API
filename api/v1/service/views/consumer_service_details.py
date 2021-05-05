from django.db import transaction
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.signals.signals import consumer_service_request_created
from v1.service.models.consumer_service_details import ServiceDetails as ServiceDetailsModel
from v1.service.serializers.consumer_service_details import ServiceDetailListSerializer, ServiceSerializer, \
    ServiceDetailViewSerializer
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, get_payload, is_authorized
from rest_framework.response import Response
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from v1.commonapp.views.logger import logger
from master.models import get_user_by_id_string
from api.messages import *
from api.constants import *

# API Header
# API end Point: api/v1/service/utility/:id_string/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Services list
# Usage: API will fetch all Services list
# Tables used: Service Deatils
# Author: Chinmay
# Created on: 4/12/2020
from v1.work_order.models.work_order_master import get_work_order_master_by_consumer_service_master_id
from v1.consumer.signals.signals import after_consumer_service_request_created
from v1.work_order.views.common_functions import set_service_appointment_data


class ServiceList(generics.ListAPIView):
    try:
        serializer_class = ServiceDetailListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ServiceDetailsModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Service Detail not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


class ConsumerServiceDetail(GenericAPIView):

    @is_token_validate
    # #role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                consumer = get_consumer_by_id_string(request.data['consumer_id_string'])
                serializer = ServiceSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    obj = serializer.create(serializer.validated_data, consumer, user)
                    obj.consumer_no = consumer.consumer_no
                    obj.save()
                    work_order = get_work_order_master_by_consumer_service_master_id(obj.consumer_service_master_id)
                    data = set_service_appointment_data(work_order, consumer)
                    # Signal for service appointment
                    consumer_service_request_created.connect(after_consumer_service_request_created)
                    consumer_service_request_created.send(consumer, data=data)
                    # Signal for service appointment
                    view_serializer = ServiceDetailViewSerializer(instance=obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Services')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)
