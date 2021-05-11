import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.constants import *
from master.models import get_user_by_id_string
from v1.commonapp.models.lifecycle import LifeCycle
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.notes import Notes
from v1.commonapp.serializers.lifecycle import LifeCycleListSerializer
from v1.commonapp.serializers.note import NoteListSerializer, NoteSerializer, NoteViewSerializer
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_master import get_consumer_by_registration_id
from v1.consumer.models.consumer_offer_master import get_consumer_offer_master_by_id_string
from v1.consumer.serializers.consumer_down_payment import ConsumerDownPaymentSerializer
from v1.consumer.serializers.consumer_master import ConsumerSerializer
from v1.consumer.serializers.consumer_offer_detail import ConsumerOfferDetailSerializer
from v1.consumer.serializers.consumer_service_contract_details import ConsumerServiceContractDetailSerializer
from v1.payment.models.payment import get_payment_by_id_string, PAYMENT_DICT
from v1.payment.models.payment_transactions import PaymentTransaction
from v1.payment.serializer.payment import *
from v1.payment.serializer.payment_transactions import PaymentTransactionListSerializer, PaymentTransactionSerializer
from v1.registration.models.registrations import Registration as RegTbl, REGISTRATION_DICT, \
    get_registration_by_registration_no
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.registration.models.registrations import get_registration_by_id_string
from v1.registration.serializers.registration import *
from v1.registration.serializers.registration_status import RegistrationStatusListSerializer
from v1.registration.signals.signals import registration_payment_approved, registration_payment_created
from api.messages import *
from v1.registration.models.registration_status import RegistrationStatus
from v1.registration.views.tasks import save_registration_timeline
from v1.userapp.decorators import is_token_validate, role_required
from django.forms.models import model_to_dict
from v1.consumer.views.common_functions import create_consumer_after_registration
from v1.commonapp.views.custom_filter_backend import CustomFilter


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
    try:
        serializer_class = RegistrationListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ( 'tenant__id_string',)
        ordering_fields = ('registration_no',)
        ordering = ('created_date',)  # always give by default alphabetical order        
        # filter_fields = ('first_name', 'tenant__id_string',)
        # ordering_fields = ('first_name', 'registration_no',)
        # ordering = ('created_date',)  # always give by default alphabetical order
        # search_fields = ('first_name', 'last_name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    queryset = RegTbl.objects.filter(is_active=True, state__in=[0,3])
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    return queryset
                else:       
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Registations')


# API Header
# API end Point: api/v1/registration
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Add registration
# Usage: Add
# Tables used: 2.4.2. Consumer - Registration
# Author: Rohan
# Created on: 23/04/2020
class Registration(GenericAPIView):

    @is_token_validate
    # #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                services = []
                transactions_reg = []
                payment = []
                offer = []
                # upfPayment = []
                # registration_obj = {}
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                registration_serializer = RegistrationSerializer(data=request.data)
                if registration_serializer.is_valid(raise_exception=False):
                    registration_obj = registration_serializer.create(registration_serializer.validated_data, user)
                    registration_obj.change_state(REGISTRATION_DICT["CREATED"])
                    registration_obj.registration_no = generate_registration_no(registration_obj)
                    if 'services' in request.data:
                        registration_obj.registration_obj['services'] = request.data.pop('services')
                    if 'transactions' in request.data:
                        transactions_reg=request.data.pop('transactions')
                        registration_obj.registration_obj['transactions'] = transactions_reg
                    if 'payment' in request.data:
                        payment=request.data.pop('payment')
                        registration_obj.registration_obj['payment'] = payment
                    # if 'offer_id' in request.data:
                    #     registration_obj.registration_obj['offer_id'] = request.data.pop('offer_id')
                    if 'offer' in request.data:
                        offer = request.data.pop('offer')
                        registration_obj.registration_obj['offer'] = offer
                    if 'upfPayment' in request.data:
                        upfPayment = request.data.pop('upfPayment')
                        registration_obj.registration_obj['upfPayment'] = upfPayment                                          
                    registration_obj.save()
                    # payment and transaction save code start
                    if payment and transactions_reg:
                        payment_serializer = PaymentSerializer(data=payment)
                        if payment_serializer.is_valid(raise_exception=True):
                            payment_obj = payment_serializer.create(payment_serializer.validated_data, registration_obj, user)
                            payment_obj.identification_id = registration_obj.id
                            payment_obj.save()
                            # # Timeline code start
                            # transaction.on_commit(
                            #     lambda: save_registration_timeline.delay(registration_obj, "Payment", "Text",
                            #                                                 "CREATED",
                            #                                                 user))
                            # # Timeline code end
                            for item in transactions_reg:
                                transaction_serializer = PaymentTransactionSerializer(data=item)
                                if transaction_serializer.is_valid(raise_exception=True):
                                    transaction_obj = transaction_serializer.create(
                                        transaction_serializer.validated_data,payment_obj,user)
                                    transaction_obj.utility = registration_obj.utility
                                    transaction_obj.tenant = registration_obj.tenant
                                    transaction_obj.payment_id = payment_obj.id
                                    transaction_obj.identification_id = registration_obj.id
                                    transaction_obj.save()
                    # payment and transaction save code end
                    view_serializer = RegistrationViewSerializer(instance=registration_obj,
                                                                 context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: list(registration_serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Registations')
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
    # #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, VIEW)
    def get(self, request, id_string):
        try:
            registration = get_registration_by_id_string(id_string)
            if "registration_no" in self.request.query_params:
                registration = get_registration_by_registration_no(self.request.query_params['registration_no'])
            if registration:
                serializer = RegistrationViewSerializer(instance=registration, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: REGISTRATION_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Registations')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            registration_obj = get_registration_by_id_string(id_string)
            if "phone_mobile" not in request.data:
                request.data['phone_mobile'] = registration_obj.phone_mobile
            if registration_obj:
                serializer = RegistrationSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    registration_obj = serializer.update(registration_obj, serializer.validated_data, user)
                    view_serializer = RegistrationViewSerializer(instance=registration_obj,
                                                                 context={'request': request})
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
                    RESULT: REGISTRATION_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Registations')
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
    #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            registration_obj = get_registration_by_id_string(id_string)
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                with transaction.atomic():
                    payment = serializer.create(serializer.validated_data, user, registration_obj)
                    view_serializer = PaymentViewSerializer(instance=payment, context={'request': request})
                    # signal to registration start
                    registration_payment_created.send(payment)
                    # signal to registration end
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
            print(e)
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Registration/payments')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            payment = get_payment_by_id_string(id_string)
            if payment:
                serializer = PaymentSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    payment = serializer.update(payment, serializer.validated_data, user)
                    view_serializer = PaymentViewSerializer(instance=payment, context={'request': request})
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
                    RESULT: PAYMENT_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Registration/payments')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/registration/payment/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Approve registration payment
# Usage: View, Update
# Tables used: 2.4.2. Consumer - Registration
# Auther: Rohan
# Created on: 25/06/2020
class RegistrationPaymentApprove(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def put(self, request, id_string):
        try:
            payment = get_payment_by_id_string(id_string)
            if payment:
                with transaction.atomic():
                    payment.change_state(PAYMENT_DICT["APPROVED"])
                    # signal to registration start
                    registration_payment_approved.send(payment)
                    # signal to registration end
                serializer = PaymentViewSerializer(instance=payment, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: PAYMENT_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Registration/payments')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/registration/payment/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Approve registration payment
# Usage: View, Update
# Tables used: 2.4.2. Consumer - Registration
# Auther: Rohan
# Created on: 25/06/2020
class RegistrationPaymentReject(GenericAPIView):

    @is_token_validate
    #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def put(self, request, id_string):
        try:
            payment = get_payment_by_id_string(id_string)
            if payment:
                with transaction.atomic():
                    # State change for payment start
                    payment.change_state(PAYMENT_DICT["REJECTED"])
                    # State change for payment end
                serializer = PaymentViewSerializer(instance=payment, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: PAYMENT_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Registration/payments')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/registration/status-list
# API verb: GET
# Package: Basic
# Modules: S & M
# Sub Module: Registration
# Interaction: Get registration statuses
# Usage: View
# Tables used: RegistrationStatus
# Auther: Rohan
# Created on: 28/09/2020
class RegistrationStatusList(generics.ListAPIView):
    try:
        serializer_class = RegistrationStatusListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    queryset = RegistrationStatus.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Registations')


# API Header
# API end Point: api/v1/registration/:id_string/reject
# API verb: Put
# Package: Basic
# Modules: S & M
# Sub Module: Registration
# Interaction: Reject registration
# Usage: View
# Tables used: Registration
# Auther: Rohan
# Created on: 28/09/2020
class RegistrationReject(GenericAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def put(self, request, id_string):
        try:
            registration = get_registration_by_id_string(id_string)
            if registration:
                with transaction.atomic():
                    # State change for registration start
                    registration.change_state(REGISTRATION_DICT["REJECTED"])
                    # State change for registration end
                serializer = RegistrationViewSerializer(instance=registration, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: REGISTRATION_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Registration')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/registration/:id_string/hold
# API verb: Put
# Package: Basic
# Modules: S & M
# Sub Module: Registration
# Interaction: Hold registration
# Usage: View
# Tables used: Registration
# Auther: Rohan
# Created on: 29/09/2020
class RegistrationHold(GenericAPIView):
    @is_token_validate
    #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def put(self, request, id_string):
        try:
            registration = get_registration_by_id_string(id_string)
            if registration:
                with transaction.atomic():
                    # State change for registration start
                    registration.change_state(REGISTRATION_DICT["HOLD"])
                    # State change for registration end
                serializer = RegistrationViewSerializer(instance=registration, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: REGISTRATION_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Registration')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/registration/:id_string/approve
# API verb: Put
# Package: Basic
# Modules: S & M
# Sub Module: Registration
# Interaction: Approve registration
# Usage: View
# Tables used: Registration
# Author: Rohan
# Created on: 30/09/2020

class RegistrationApprove(GenericAPIView):
    @is_token_validate
    # #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            registration = get_registration_by_id_string(id_string)
            if registration:
                with transaction.atomic():
                    # service=[]                  
                    consumer = create_consumer_after_registration(registration.id)

                    service_new=[]
                    if 'services' in registration.registration_obj:
                        service_new=registration.registration_obj['services']

                    transaction_new=[]
                    payment=[]
                    if 'transactions' and 'payment' in registration.registration_obj:
                        transaction_new=registration.registration_obj['transactions']
                        payment=registration.registration_obj['payment'] 

                    upfPayment=[]
                    if 'upfPayment' in registration.registration_obj:    
                        upfPayment=registration.registration_obj['upfPayment']

                    # offer_id=[]
                    # if 'offer_id' in registration.registration_obj:    
                    #     offer_id={'offer_id':registration.registration_obj['offer_id']}
                    #     print("===OFFER_ID=====",offer_id)

                    offer=[]
                    if 'offer' in registration.registration_obj:    
                        offer=registration.registration_obj['offer']

                     # Consumer service contract details save start
                    if service_new and offer:
                        for service_obj in service_new:
                            consumer_service_contract_serializer = ConsumerServiceContractDetailSerializer(
                                data=service_obj)
                            consumer_service_contract_serializer.is_valid(raise_exception=False)
                            contract_detail_obj = consumer_service_contract_serializer.create(
                                consumer_service_contract_serializer.validated_data, consumer, user)
                            contract_detail_obj.is_active=False
                            contract_detail_obj.save()
                            product_id=service_obj['product_id']
                            
                            for offer_obj in offer:
                                if offer_obj['product_id']==product_id:
                                    consumer_offer_detail_serializer = ConsumerOfferDetailSerializer(data=offer_obj)
                                    consumer_offer_detail_serializer.is_valid(raise_exception=True)
                                    consumer_offer_detail_obj = consumer_offer_detail_serializer.create(
                                        consumer_offer_detail_serializer.validated_data, consumer, user)
                                    offer_contract=offer_obj['offer_id']
                                    consumer_offer_detail_obj.offer_id = get_consumer_offer_master_by_id_string(
                                        offer_contract).id
                                    consumer_offer_detail_obj.consumer_service_contract_detail_id = contract_detail_obj.id
                                    consumer_offer_detail_obj.save()


                        # if contract_detail_obj:
                        #     for offer_obj in offer:
                        #         print("==++++++++======++++++++++++++++",offer_obj)
                        #         consumer_offer_detail_serializer = ConsumerOfferDetailSerializer(data=offer_obj)
                        #         consumer_offer_detail_serializer.is_valid(raise_exception=True)
                        #         consumer_offer_detail_obj = consumer_offer_detail_serializer.create(
                        #             consumer_offer_detail_serializer.validated_data, consumer, user)
                        #         print("*****************CREATED SUCCESSFULLY************************************")
                        #         print("==========OFFER OBJ===============",offer_obj)
                        #         offer=offer_obj['offer_id']
                        #         consumer_offer_detail_obj.offer_id = get_consumer_offer_master_by_id_string(
                        #             offer).id
                        #         consumer_offer_detail_obj.consumer_service_contract_detail_id = contract_detail_obj.id
                        #         consumer_offer_detail_obj.save()
                    # Consumer service contract details save end

                    # payment and transaction save code start
                    if payment and transaction_new:
                        payment_serializer = PaymentSerializer(data=payment)
                        if payment_serializer.is_valid(raise_exception=False):
                            payment_obj = payment_serializer.create(payment_serializer.validated_data,
                                                                    consumer,
                                                                    user)
                            payment_obj.consumer_no = consumer.consumer_no
                            payment_obj.save()
                            for item in transaction_new:
                                transaction_serializer = PaymentTransactionSerializer(data=item)
                                if transaction_serializer.is_valid(raise_exception=True):
                                    transaction_obj = transaction_serializer.create(
                                        transaction_serializer.validated_data, payment_obj, user)
                    # payment and transaction save code end
                    
                    # upfront payment save code start
                    if upfPayment !='':
                        consumer_down_payment_serializer = ConsumerDownPaymentSerializer(
                            data=upfPayment)
                        consumer_down_payment_serializer.is_valid()
                        consumer_down_payment_obj = consumer_down_payment_serializer.create(
                            consumer_down_payment_serializer.validated_data, consumer, user)
                        consumer_down_payment_obj.collected_amount = upfPayment
                        consumer.is_upfront_amount = True
                        consumer_down_payment_obj.save()  
                    # upfront payment save code start

                    # Consumer offer detail save code start
                    # if offer:
                    #     for offer_obj in offer:
                    #         print("==++++++++======++++++++++++++++",offer_obj)
                    #         consumer_offer_detail_serializer = ConsumerOfferDetailSerializer(data=offer_obj)
                    #         consumer_offer_detail_serializer.is_valid(raise_exception=True)
                    #         consumer_offer_detail_obj = consumer_offer_detail_serializer.create(
                    #             consumer_offer_detail_serializer.validated_data, consumer, user)
                    #         print("*****************CREATED SUCCESSFULLY************************************")
                    #         print("==========OFFER OBJ===============",offer_obj)
                    #         offer=offer_obj['offer_id']
                    #         consumer_offer_detail_obj.offer_id = get_consumer_offer_master_by_id_string(
                    #             offer).id
                    #         consumer_offer_detail_obj.save()
                    #         # Consumer offer detail save code end

                    
                                    
                    # State change for registration start
                    registration.change_state(REGISTRATION_DICT["APPROVED"])
                    # State change for registration end
                    # # Timeline code start
                    # transaction.on_commit(
                    #     lambda: save_registration_timeline.delay(registration, "Registration", "Text", "Approved",
                    #                                              user))
                    # # Timeline code end
                serializer = RegistrationViewSerializer(instance=registration, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: REGISTRATION_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("eroor===",e)
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Registration')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)

# API Header
# API end Point: api/v1/registration/:id_string/notes
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Registration notes
# Usage: API will fetch required data for Registration notes
# Tables used: Notes
# Author: Rohan
# Created on: 1/10/2020
class RegistrationNoteList(generics.ListAPIView):
    try:
        serializer_class = NoteListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    registration = get_registration_by_id_string(self.kwargs['id_string'])
                    queryset = Notes.objects.filter(identification_id=registration.id, is_active=True)
                    print("========queryset=====",queryset)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Notes not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Registration')


# API Header
# API end Point: api/v1/registration/:id_string/note
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Add registration note
# Usage: Add
# Tables used: Note
# Auther: Rohan
# Created on: 05/10/2020
class RegistrationNote(GenericAPIView):

    @is_token_validate
    # #role_required(CONSUMER_OPS, CONSUMER_OPS_REGISTRATION, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            registration = get_registration_by_id_string((id_string))
            module = get_module_by_key("CX")
            print("======module======",module)
            sub_module = get_sub_module_by_key("REGISTRATION")
            print("===submodule====",sub_module)
            print("====request data======",request.data)
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                note_obj = serializer.create(serializer.validated_data, user)
                note_obj.identification_id = registration.id
                note_obj.tenant = registration.tenant
                note_obj.utility = registration.utility
                note_obj.module_id = module
                note_obj.sub_module_id = sub_module
                note_obj.save()
                view_serializer = NoteViewSerializer(instance=note_obj, context={'request': request})
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
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Registration')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/registration/:id_string/payments
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Registration payments
# Usage: API will fetch required data for Registration payments
# Tables used: Consumer Payment
# Author: Rohan
# Created on: 6/10/2020
class RegistrationPaymentList(generics.ListAPIView):
    try:
        serializer_class = PaymentListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    registration = get_registration_by_id_string(self.kwargs['id_string'])
                    queryset = Payment.objects.filter(identification_id = registration.id)
                    print(queryset)
                    # consumer = get_consumer_by_registration_id(registration.id)
                    # queryset = Payment.objects.filter(consumer_no = consumer.consumer_no)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Payments not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        print("error===========",e)
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Registration')


# API Header
# API end Point: api/v1/registration/:id_string/life-cycles
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Registration lifecycles
# Usage: API will fetch required data for Registration lifecycles
# Tables used: LifeCycles
# Author: Rohan
# Created on: 28/10/2020
class RegistrationLifeCycleList(generics.ListAPIView):
    try:
        serializer_class = LifeCycleListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    # module = get_module_by_key("CONSUMER_OPS")
                    # sub_module = get_sub_module_by_key("CONSUMER_OPS_REGISTRATION")
                    module = get_module_by_key("CX")
                    sub_module = get_sub_module_by_key("REGISTRATION")
                    queryset = ""
                    if 'registration_id' in self.request.query_params:
                        registration = get_registration_by_id_string(self.request.query_params['registration_id'])
                        queryset = LifeCycle.objects.filter(object_id=registration.id, module_id=module, sub_module_id=sub_module, is_active=True)
                    if 'registration_no' in self.request.query_params:
                        registration = get_registration_by_registration_no(self.request.query_params['registration_no'])
                        queryset = LifeCycle.objects.filter(object_id=registration.id, module_id=module, sub_module_id=sub_module, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Lifecycles not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Registration')


# API Header
# API end Point: api/v1/registration/:id_string/payment-transactions
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Registration
# Interaction: Registration Payment Transactions
# Usage: API will fetch required data for Registration payment transactions
# Tables used: Payment Transaction
# Author: Rohan
# Created on: 28/10/2020
class RegistrationPaymentTransactionList(generics.ListAPIView):
    try:
        serializer_class = PaymentTransactionListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    payment = get_payment_by_id_string(self.kwargs['id_string'])
                    queryset = PaymentTransaction.objects.filter(payment_id = payment.id)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Transactions not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Registration')