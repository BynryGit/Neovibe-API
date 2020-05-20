from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.payment.models.consumer_payment import get_payment_by_id_string
from v1.payment.serializer.payment import PaymentSerializer, PaymentViewSerializer
from v1.registration.models.registrations import Registration as RegTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.registration.serializers.registration import RegistrationViewSerializer, RegistrationSerializer, \
    RegistrationListSerializer
from v1.userapp.models.user_master import UserDetail
from v1.registration.models.registrations import get_registration_by_id_string
from v1.registration.views.common_functions import is_data_verified
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS


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
class RegistrationList(generics.ListAPIView):
    serializer_class = RegistrationListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('first_name', 'tenant__id_string',)
    ordering_fields = ('first_name', 'registration_no',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('first_name', 'email_id',)

    def get_queryset(self):
        if is_token_valid(self.request.headers['token']):
            if is_authorized():
                queryset = RegTbl.objects.filter(is_active=True)
                return queryset




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

    def post(self, request):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    user = UserDetail.objects.get(id = 2)
                    if is_data_verified(request):
                    # Request data verification end
                        serializer = RegistrationSerializer(data=request.data)
                        if serializer.is_valid():
                            registration_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = RegistrationViewSerializer(instance=registration_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
                            }, status=status.HTTP_201_CREATED)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

    def get(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    registration = get_registration_by_id_string(id_string)
                    if registration:
                        serializer = RegistrationViewSerializer(instance=registration, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        user = UserDetail.objects.get(id=2)
                        registration_obj = get_registration_by_id_string(id_string)
                        if registration_obj:
                            serializer = RegistrationSerializer(data=request.data)
                            if serializer.is_valid(request.data):
                                registration_obj = serializer.update(registration_obj, serializer.validated_data, user)
                                view_serializer = RegistrationViewSerializer(instance=registration_obj,
                                                                             context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULTS: view_serializer.data,
                                }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                            }, status=status.HTTP_404_NOT_FOUND)
                        # Save basic details start
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,

                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

     def post(self, request, id_string):
         try:
             if is_token_valid(request.headers['token']):
                 if is_authorized():
                     if is_data_verified(request):
                         user = UserDetail.objects.get(id=2)
                         registration_obj = get_registration_by_id_string(id_string)
                         serializer = PaymentSerializer(data=request.data)
                         if serializer.is_valid():
                             payment = serializer.create(serializer.validated_data, user, registration_obj)
                             view_serializer = PaymentViewSerializer(instance=payment, context={'request': request})
                             return Response({
                                 STATE: SUCCESS,
                                 RESULTS: view_serializer.data,
                             }, status=status.HTTP_201_CREATED)
                         else:
                             return Response({
                                 STATE: ERROR,
                                 RESULTS: serializer.errors,
                             }, status=status.HTTP_400_BAD_REQUEST)
                     else:
                         return Response({
                             STATE: ERROR,
                         }, status=status.HTTP_400_BAD_REQUEST)
                 else:
                     return Response({
                         STATE: ERROR,
                     }, status=status.HTTP_403_FORBIDDEN)
             else:
                 return Response({
                     STATE: ERROR,
                 }, status=status.HTTP_401_UNAUTHORIZED)
         except Exception as e:
             logger().log(e, 'ERROR', user='test', name='test')
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

    def get(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    payment = get_payment_by_id_string(id_string)
                    if payment:
                        serializer = PaymentViewSerializer(instance=payment, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        user = UserDetail.objects.get(id=2)
                        payment = get_payment_by_id_string(id_string)
                        if payment:
                            serializer = PaymentSerializer(data=request.data)
                            if serializer.is_valid(request.data):
                                payment = serializer.update(payment, serializer.validated_data, user)
                                view_serializer = PaymentViewSerializer(instance=payment,
                                                                             context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULTS: view_serializer.data,
                                }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                            }, status=status.HTTP_404_NOT_FOUND)
                        # Save basic details start
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,

                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


