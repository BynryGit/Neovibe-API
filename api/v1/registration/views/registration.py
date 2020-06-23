import traceback

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.constants import *
from master.models import User, get_user_by_id_string
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_master import get_consumer_by_registration_id
from v1.payment.models.consumer_payment import get_payment_by_id_string
from v1.payment.serializer.payment import PaymentSerializer, PaymentViewSerializer
from v1.registration.models.registrations import Registration as RegTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.registration.models.registrations import get_registration_by_id_string
from v1.registration.serializers.registration import *
from v1.registration.views.common_functions import is_data_verified
from api.messages import *


# API Header
# API end Point: api/v1/registration/list
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Registration list
# Usage: API will fetch required data for Registration list
# Tables used: 2.4.2. Consumer - Registration
# Author: Rohan
# Created on: 21/04/2020
from v1.userapp.decorators import is_token_validate, role_required


class RegistrationList(generics.ListAPIView):
    try:
        serializer_class = RegistrationListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('first_name', 'tenant__id_string',)
        ordering_fields = ('first_name', 'registration_no',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('first_name', 'last_name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = RegTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'ERROR')
        # raise APIException




# API Header
# API end Point: api/v1/registration
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Add registration
# Usage: Add
# Tables used: 2.4.2. Consumer - Registration
# Auther: Rohan
# Created on: 23/04/2020
class Registration(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, REGISTRATION, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                registration_obj = serializer.create(serializer.validated_data, user)
                view_serializer = RegistrationViewSerializer(instance=registration_obj, context={'request': request})
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
            logger().log(e, 'ERROR', module = 'Consumer Ops', sub_module = 'Registations')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/registration/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Add, Update registration
# Usage: Add
# Tables used: 2.4.2. Consumer - Registration
# Auther: Rohan
# Created on: 23/04/2020
class RegistrationDetail(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, REGISTRATION, VIEW)
    def get(self, request, id_string):
        try:
            registration = get_registration_by_id_string(id_string)
            if registration:
                serializer = RegistrationViewSerializer(instance=registration, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: DATA_NOT_EXISTS,
                }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger().log(e, 'ERROR', module = 'Consumer Ops', sub_module = 'Registations')
            return Response({
                STATE: EXCEPTION,
                RESULT: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(CONSUMER_OPS, REGISTRATION, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            registration_obj = get_registration_by_id_string(id_string)
            if "phone_mobile" not in request.data:
                request.data['phone_mobile'] = registration_obj.phone_mobile
            if registration_obj:
                serializer = RegistrationSerializer(data=request.data)
                if serializer.is_valid(request.data):
                    registration_obj = serializer.update(registration_obj, serializer.validated_data, user)
                    view_serializer = RegistrationViewSerializer(instance=registration_obj,
                                                                 context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                    }, status=status.HTTP_200_OK)
            # Save basic details end
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'ERROR', module = 'Consumer Ops', sub_module = 'Registations')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/registration/:id_string/payment
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Add registration payment
# Usage: Add
# Tables used: 2.4.2. Consumer - Registration
# Auther: Rohan
# Created on: 18/05/2020
class RegistrationPayment(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, REGISTRATION, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            registration_obj = get_registration_by_id_string(id_string)
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                payment = serializer.create(serializer.validated_data, user, registration_obj)
                view_serializer = PaymentViewSerializer(instance=payment, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'ERROR', module = 'Consumer Ops', Sub_module='Registration/payments')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/registration/payment/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: View, Update registration payment
# Usage: View, Update
# Tables used: 2.4.2. Consumer - Registration
# Auther: Rohan
# Created on: 18/05/2020
class RegistrationPaymentDetail(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, REGISTRATION, VIEW)
    def get(self, request, id_string):
        try:
            payment = get_payment_by_id_string(id_string)
            if payment:
                serializer = PaymentViewSerializer(instance=payment, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    RESULT: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger().log(e, 'ERROR', module = 'Consumer Ops', Sub_module='Registration/payments')
            return Response({
                STATE: EXCEPTION,
                RESULT: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(CONSUMER_OPS, REGISTRATION, EDIT)
    def put(self, request, id_string):
        try:
            # Save basic details start
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            payment = get_payment_by_id_string(id_string)
            if payment:
                serializer = PaymentSerializer(data=request.data)
                if serializer.is_valid(request.data):
                    payment = serializer.update(payment, serializer.validated_data, user)
                    view_serializer = PaymentViewSerializer(instance=payment, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: 'Payment not found!'
                }, status=status.HTTP_404_NOT_FOUND)
            # Save basic details start
        except Exception as e:
            logger().log(e, 'ERROR', module = 'Consumer Ops', Sub_module='Registration/payments')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


