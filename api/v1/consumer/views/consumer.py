from typing import FrozenSet
from v1.work_order.models.work_order_master import WorkOrderMaster, get_work_order_master_by_id_string
from v1.commonapp.views.notifications import send_sms
from v1.utility.models.utility_work_order_sub_type import UtilityWorkOrderSubType, get_utility_work_order_sub_type_by_id
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.constants import *
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.models.invoice_bill import get_invoice_bills_by_consumer_no, get_invoice_bill_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.models.notes import Notes
from v1.commonapp.serializers.note import NoteSerializer, NoteViewSerializer, NoteListSerializer
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.consumer.models.consumer_category import ConsumerCategory, get_consumer_category_by_id_string
from v1.consumer.models.consumer_master import get_consumer_by_id_string, ConsumerMaster
from v1.consumer.models.consumer_offer_master import get_consumer_offer_master_by_id_string
from v1.consumer.models.consumer_ownership import ConsumerOwnership
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_sub_category import ConsumerSubCategory
from v1.consumer.serializers.consumer_down_payment import ConsumerDownPaymentSerializer
from v1.consumer.serializers.consumer_master import ConsumerSerializer, ConsumerViewSerializer, ConsumerListSerializer
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_offer_detail import ConsumerOfferDetailSerializer
from v1.consumer.serializers.consumer_ownership import ConsumerOwnershipListSerializer
from v1.consumer.serializers.consumer_personal_detail import ConsumerPersonalDetailSerializer
from v1.consumer.serializers.consumer_scheme_master import *
from v1.consumer.serializers.consumer_service_contract_details import ConsumerServiceContractDetailSerializer
from v1.consumer.views.tasks import save_consumer_audit_log
from v1.meter_data_management.models.meter import get_meter_by_id_string
from v1.payment.models.payment import get_payments_by_consumer_no, get_payment_by_id_string
from v1.payment.serializer.payment import *
from v1.payment.serializer.payment_transactions import PaymentTransactionSerializer
from v1.service.models.consumer_service_details import get_consumer_services_by_consumer_no
from v1.service.serializers.consumer_service_details import ServiceDetailListSerializer
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.complaint.models.complaint import Complaint
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.utility.models.utility_product import get_utility_product_by_id
from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id
from v1.commonapp.models.work_order_type import WorkOrderType, get_work_order_type_by_key
from v1.utility.models.utility_work_order_type import UtilityWorkOrderType, get_utility_work_order_type_by_id
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id_string
from v1.commonapp.models.work_order_sub_type import get_work_order_sub_type_by_key
from django.db import Q
from v1.work_order.models.service_appointments import ServiceAppointment as ServiceAppointmentTbl
# API Header
# API end Point: api/v1/consumer/:id_string/list
# API verb: GET
# Interaction: Consumer list
# Usage: API will fetch all Consumer List
# Tables used: Consumer master
# Author: Rohan
# Created on: 22/12/2020
from v1.utility.models.utility_product import get_utility_product_by_id_string
from v1.work_order.serializers.service_appointment import ServiceAppointmentSerializer
from v1.work_order.views.common_functions import generate_service_appointment_no


class ConsumerList(generics.ListAPIView):
    try:
        serializer_class = ConsumerListSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('consumer_no', 'tenant__id_string',)
        ordering_fields = ('consumer_no', 'tenant',)
        ordering = ('consumer_no',)  # always give by default alphabetical order
        search_fields = ('consumer_no', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerMaster.objects.filter(utility=utility, is_active=True)
                    if "consumer_no" in self.request.query_params:
                        queryset = queryset.filter(consumer_no=self.request.query_params['consumer_no'])
                    if "email_id" in self.request.query_params:
                        queryset = queryset.filter(email_id=self.request.query_params['email_id'])
                    if "phone_mobile" in self.request.query_params:
                        queryset = queryset.filter(phone_mobile=self.request.query_params['phone_mobile'])
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
# API end Point: api/v1/consumer
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Add
# Usage: Add
# Tables used: ConsumerMaster
# Author: Rohan
# Created on: 19/05/2020
class Consumer(GenericAPIView):
    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                services = []
                transactions = []
                payment = {}
                account_holders = []
                if 'services' in request.data:
                    services = request.data.pop('services')
                if 'transactions' in request.data:
                    transactions = request.data.pop('transactions')
                if 'account_holders' in request.data:
                    account_holders = request.data.pop('account_holders')
                if 'payment' in request.data:
                    payment = request.data.pop('payment')
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                consumer_serializer = ConsumerSerializer(data=request.data)
                if consumer_serializer.is_valid(raise_exception=True):
                    consumer_obj = consumer_serializer.create(consumer_serializer.validated_data, user)
                    # Consumer service contract details save start
                    if services:
                        for service in services:
                            consumer_service_contract_serializer = ConsumerServiceContractDetailSerializer(data=service)
                            consumer_service_contract_serializer.is_valid()
                            contract_detail_obj = consumer_service_contract_serializer.create(
                                consumer_service_contract_serializer.validated_data, consumer_obj, user)
                            if service['is_new_meter'] == 'False':
                                meter = get_meter_by_id_string(service['existing_meter_id'])
                                contract_detail_obj.meter_id = meter.id
                            contract_detail_obj.save()
                            # Consumer service contract details save end
                    # payment and transaction save code start
                    if payment and transactions:
                        payment_serializer = PaymentSerializer(data=payment)
                        if payment_serializer.is_valid(raise_exception=True):
                            payment_obj = payment_serializer.create(payment_serializer.validated_data, consumer_obj,
                                                                    user)
                            payment_obj.consumer_no = consumer_obj.consumer_no
                            payment_obj.save()
                            for item in transactions:
                                transaction_serializer = PaymentTransactionSerializer(data=item)
                                if transaction_serializer.is_valid(raise_exception=True):
                                    transaction_obj = transaction_serializer.create(
                                        transaction_serializer.validated_data, payment_obj, user)
                                    # payment and transaction save code end
                    # upfront payment save code start
                    if 'upfPayment' in request.data:
                        request.data['upfPayment'] = request.data['upfPayment'].strip()
                        if request.data['upfPayment'] != '':
                            consumer_down_payment_serializer = ConsumerDownPaymentSerializer(data=request.data)
                            consumer_down_payment_serializer.is_valid()
                            consumer_down_payment_obj = consumer_down_payment_serializer.create(
                                consumer_down_payment_serializer.validated_data, consumer_obj, user)
                            consumer_down_payment_obj.collected_amount = request.data['upfPayment']
                            consumer_obj.is_upfront_amount = True
                            consumer_down_payment_obj.save()
                            # upfront payment save code start
                    # Consumer offer detail save code start
                    if 'offer_id' in request.data:
                        consumer_offer_detail_serializer = ConsumerOfferDetailSerializer(data=request.data)
                        consumer_offer_detail_serializer.is_valid()
                        consumer_offer_detail_obj = consumer_offer_detail_serializer.create(
                            consumer_offer_detail_serializer.validated_data, consumer_obj, user)
                        consumer_offer_detail_obj.offer_id = get_consumer_offer_master_by_id_string(
                            request.data['offer_id']).id
                        consumer_offer_detail_obj.save()
                        # Consumer offer detail save code end
                    if account_holders:
                        for account_holder in account_holders:
                            consumer_personal_detail_serializer = ConsumerPersonalDetailSerializer(data=account_holder)
                            if consumer_personal_detail_serializer.is_valid(raise_exception=True):
                                consumer_personal_detail_obj = consumer_personal_detail_serializer.create(
                                    consumer_personal_detail_serializer.validated_data, consumer_obj, user)
                    view_serializer = ConsumerViewSerializer(instance=consumer_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: list(consumer_serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Get, Update
# Usage: Add
# Tables used: ConsumerMaster
# Author: Rohan
# Created on: 19/05/2020
class ConsumerDetail(GenericAPIView):

    # @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER, VIEW)
    def get(self, request, id_string):
        try:
            consumer = get_consumer_by_id_string(id_string)
            if consumer:
                serializer = ConsumerViewSerializer(instance=consumer, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    RESULT: CONSUMER_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Consumer Ops', Sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def put(self, request, id_string):
        try:
            with transaction.atomic():
                remark = request.data['remark'] if 'remark' in request.data else ""
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                consumer = get_consumer_by_id_string(id_string)
                if consumer:
                    if "phone_mobile" not in request.data:
                        request.data["phone_mobile"] = consumer.phone_mobile
                    serializer = ConsumerSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        if 'email_id' in request.data:
                            # Audit log code start
                            save_consumer_audit_log(consumer, "email_id", consumer.email_id, request.data['email_id'],
                                                    remark, user)
                            # Audit log code end
                        if 'billing_address_line_1' in request.data:
                            # Audit log code start
                            save_consumer_audit_log(consumer, "billing_address_line_1", consumer.billing_address_line_1,
                                                    request.data['billing_address_line_1'], remark, user)
                            # Audit log code end
                        if 'mobile_change' in request.data:
                            # Audit log code start
                            save_consumer_audit_log(consumer, "phone_mobile", consumer.phone_mobile,
                                                    request.data['phone_mobile'], remark, user)
                            # Audit log code end
                        consumer_obj = serializer.update(consumer, serializer.validated_data, user)
                        view_serializer = ConsumerViewSerializer(instance=consumer_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: view_serializer.data,
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: CONSUMER_NOT_FOUND,
                    }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("############", e)
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/:id_string/bill/list
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Bill list
# Usage: API will fetch required data for Bill list
# Tables used: InvoiceBill, ConsumerMaster
# Author: Rohan
# Created on: 20/05/2020
class ConsumerBillList(generics.ListAPIView):
    try:
        serializer_class = InvoiceBillListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('bill_month', 'tenant__id_string',)
        ordering_fields = ('bill_month',)
        ordering = ('bill_month',)  # always give by default alphabetical order
        search_fields = ('bill_month',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    consumer = get_consumer_by_id_string(self.kwargs['id_string'])
                    if consumer:
                        queryset = get_invoice_bills_by_consumer_no(consumer.consumer_no)
                        return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/consumer/:id_string/payment/list
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Payment list
# Usage: API will fetch required data for Payment list
# Tables used: Payment, ConsumerMaster
# Author: Rohan
# Created on: 21/05/2020
class ConsumerPaymentList(generics.ListAPIView):
    try:
        serializer_class = PaymentListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('transaction_date',)
        ordering_fields = ('transaction_date',)
        ordering = ('transaction_date',)
        search_fields = ('transaction_amount',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    consumer = get_consumer_by_id_string(self.kwargs['id_string'])
                    if consumer:
                        queryset = get_payments_by_consumer_no(consumer.consumer_no)
                        return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/consumer/:id_string/complaint/list
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Complaint list
# Usage: API will fetch required data for Complaint list
# Tables used: ConsumerComplaint, ConsumerMaster
# Author: Rohan
# Created on: 21/05/2020
# class ConsumerComplaintList(generics.ListAPIView):
#     try:
#         serializer_class = ComplaintListSerializer
#         pagination_class = StandardResultsSetPagination

#         filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
#         filter_fields = ('complaint_date',)
#         ordering_fields = ('complaint_date',)
#         ordering = ('complaint_date',)  # always give by default alphabetical order
#         search_fields = ('complaint_date',)

#         def get_queryset(self):
#             if is_token_valid(self.request.headers['token']):
#                 if is_authorized():
#                     consumer = get_consumer_by_id_string(self.kwargs['id_string'])
#                     if consumer:
#                         queryset = get_consumer_complaints_by_consumer_no(consumer.consumer_no)
#                         return queryset
#                     else:
#                         raise InvalidAuthorizationException
#                 else:
#                     raise InvalidTokenException
#     except Exception as e:
#         logger().log(e, 'ERROR')
#         raise APIException


class ConsumerComplaintList(generics.ListAPIView):
    try:
        serializer_class = ComplaintListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('complaint_date',)
        ordering_fields = ('complaint_date',)
        ordering = ('complaint_date',)  # always give by default alphabetical order
        search_fields = ('complaint_date',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = Complaint.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer Complaint master not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Complaint', sub_module='Complaint')




# API Header
# API end Point: api/v1/consumer/:id_string/service/list
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Service list
# Usage: API will fetch required data for Complaint list
# Tables used: ConsumerService, ConsumerMaster
# Author: Rohan
# Created on: 21/05/2020
class ConsumerServiceList(generics.ListAPIView):
    try:
        serializer_class = ServiceDetailListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('request_date',)
        ordering_fields = ('request_date',)
        ordering = ('request_date',)
        search_fields = ('request_date',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    consumer = get_consumer_by_id_string(self.kwargs['id_string'])
                    if consumer:
                        queryset = get_consumer_services_by_consumer_no(consumer.consumer_no)
                        return queryset
                    else:
                        raise InvalidAuthorizationException
                else:
                    raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/consumer/bill/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Get, Update
# Usage: Get, Update
# Tables used: ConsumerMaster, InvoiceBill
# Auther: Rohan
# Created on: 20/05/2020
class ConsumerBillDetail(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, VIEW)
    def get(self, request, id_string):
        try:
            bill = get_invoice_bill_by_id_string(id_string)
            if bill:
                serializer = InvoiceBillViewSerializer(instance=bill, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: BILL_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Consumer Ops', Sub_module='Consumer/Bill')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            bill = get_invoice_bill_by_id_string(id_string)
            if bill:
                serializer = InvoiceBillSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    bill = serializer.update(bill, serializer.validated_data, user)
                    view_serializer = InvoiceBillViewSerializer(instance=bill, context={'request': request})
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
                    RESULT: BILL_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Consumer/Bill')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/:id_string/payment
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Add consumer payment
# Usage: Add
# Tables used: Payment
# Auther: Rohan
# Created on: 21/05/2020
class ConsumerPayment(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            consumer_obj = get_consumer_by_id_string(id_string)
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                payment = serializer.create(serializer.validated_data, user, consumer_obj)
                view_serializer = PaymentViewSerializer(instance=payment, context={'request': request})
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
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Consumer/payments')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/payment/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: View, Update consumer payment
# Usage: View, Update
# Tables used: Payment
# Auther: Rohan
# Created on: 21/05/2020
class ConsumerPaymentDetail(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, VIEW)
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
                    STATE: ERROR,
                    RESULT: DATA_NOT_EXISTS,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Consumer/payments')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, EDIT)
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
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: PAYMENT_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Consumer/payments')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/:id_string/complaint
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Add consumer complaint
# Usage: Add
# Tables used: Consumer Complaint
# Author: Rohan
# Created on: 22/05/2020
class ConsumerComplaint(GenericAPIView):

    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            consumer_obj = get_consumer_by_id_string(request.data['consumer_id_string'])
            request.data['consumer_no'] = consumer_obj.consumer_no
            serializer = ComplaintSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                complaint = serializer.create(serializer.validated_data, consumer_obj, user)
                view_serializer = ComplaintViewSerializer(instance=complaint, context={'request': request})
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
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Consumer/complaint')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/complaint/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: View, Update consumer complaint
# Usage: View, Update
# Tables used: CosumerComlaint
# Auther: Rohan
# Created on: 22/05/2020
class ConsumerComplaintDetail(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, VIEW)
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
            logger().log(e, 'MEDIUM', module='Consumer Ops', Sub_module='Consumer/complaint')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            complaint = get_consumer_complaint_by_id_string(id_string)
            if complaint:
                serializer = ComplaintSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    complaint = serializer.update(complaint, serializer.validated_data, user)
                    view_serializer = ComplaintViewSerializer(instance=complaint, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: COMPLAINT_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Consumer Ops', Sub_module='Consumer/complaint')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/:id_string/scheme
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Add consumer scheme
# Usage: Add
# Tables used: CosumerSchemeMaster
# Auther: Rohan
# Created on: 23/05/2020
class ConsumerScheme(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            consumer_obj = get_consumer_by_id_string(id_string)
            serializer = ConsumerSchemeMasterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                scheme = serializer.create(serializer.validated_data, user)
                consumer_obj.scheme_id = scheme.id
                consumer_obj.save()
                view_serializer = ConsumerSchemeMasterViewSerializer(instance=scheme, context={'request': request})
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
            logger().log(e, 'MEDIUM', module='Consumer Ops', Sub_module='Consumer/scheme')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/scheme/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: View, Update consumer scheme
# Usage: View, Update
# Tables used: CosumerSchemeMaster
# Auther: Rohan
# Created on: 23/05/2020
class ConsumerSchemeDetail(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, VIEW)
    def get(self, request, id_string):
        try:
            scheme = get_scheme_by_id_string(id_string)
            if scheme:
                serializer = ConsumerSchemeMasterViewSerializer(instance=scheme, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: SCHEME_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Consumer Ops', Sub_module='Consumer/scheme')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def put(self, request, id_string):
        try:
            scheme = get_scheme_by_id_string(id_string)
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            if scheme:
                serializer = ConsumerSchemeMasterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    scheme = serializer.update(scheme, serializer.validated_data, user)
                    view_serializer = ConsumerSchemeMasterViewSerializer(instance=scheme, context={'request': request})
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
                    RESULT: SCHEME_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Consumer Ops', Sub_module='Consumer/scheme')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/:id_string/categories
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Consumer categories
# Usage: API will fetch required data for Consumer categories
# Tables used: Consumer category
# Author: Rohan
# Created on: 09/10/2020
class ConsumerCategoryList(generics.ListAPIView):
    try:
        serializer_class = ConsumerCategoryListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerCategory.objects.filter(utility=utility, is_active=True)
                    if "product_id" in self.request.query_params:
                        product = get_utility_product_by_id_string(self.request.query_params['product_id'])
                        queryset = queryset.filter(product_id=product.id)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer categories not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Consumer')


# API Header
# API end Point: api/v1/consumer/:id_string/sub-categories
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Consumer sub categories
# Usage: API will fetch required data for Consumer sub categories
# Tables used: Consumer sub category
# Author: Rohan
# Created on: 09/10/2020
class ConsumerSubCategoryList(generics.ListAPIView):
    try:
        serializer_class = ConsumerSubCategoryListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerSubCategory.objects.filter(utility=utility, is_active=True)
                    if 'category_id' in self.request.query_params:
                        category = get_consumer_category_by_id_string(self.request.query_params['category_id'])
                        queryset = queryset.filter(category_id=category.id)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer sub categories not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Consumer')


# API Header
# API end Point: api/v1/consumer/:id_string/ownerships
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Consumer ownerships
# Usage: API will fetch required data for Consumer ownerships
# Tables used: Consumer ownership
# Author: Rohan
# Created on: 09/10/2020
class ConsumerOwnershipList(generics.ListAPIView):
    try:
        serializer_class = ConsumerOwnershipListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerOwnership.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer ownership not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Consumer')


# API Header
# API end Point: api/v1/consumer/:id_string/note
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Add consumer note
# Usage: Add
# Tables used: Note
# Author: Rohan
# Created on: 11/01/2021
class ConsumerNote(GenericAPIView):

    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER_OPS_CONSUMER, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            consumer = get_consumer_by_id_string(id_string)
            module = get_module_by_key("CONSUMEROPS")
            sub_module = get_sub_module_by_key("CONSUMER")
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                note_obj = serializer.create(serializer.validated_data, user)
                note_obj.identification_id = consumer.id
                note_obj.tenant = consumer.tenant
                note_obj.utility = consumer.utility
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
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/:id_string/note/list
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Add Consumer note
# Usage: Add
# Tables used: Note
# Author: Rohan
# Created on: 11/01/2021
class ConsumerNoteList(generics.ListAPIView):
    try:
        serializer_class = NoteListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    consumer = get_consumer_by_id_string(self.kwargs['id_string'])
                    queryset = Notes.objects.filter(identification_id=consumer.id, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Notes not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer Ops', sub_module='Consumer')


from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.logger import logger
from v1.consumer.models.consumer_master import get_consumer_by_id_string, CONSUMER_DICT
from v1.consumer.serializers.consumer_master import ConsumerViewSerializer
from v1.userapp.decorators import is_token_validate


# API Header
# API end Point: api/v1/consumer/approve
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Approve
# Usage: Approve
# Tables used: ConsumerMaster
# Author: Rohan
# Created on: 29-01-2021
class ConsumerApprove(GenericAPIView):

    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                consumer = get_consumer_by_id_string(request.data['consumer_id'])
                # State change for consumer start
                consumer.change_state(CONSUMER_DICT["APPROVED"])
                # State change for consumer end
                appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                if appointment_serializer.is_valid(raise_exception=True):
                    appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                    appointment_obj.utility = consumer.utility
                    appointment_obj.sa_number = generate_service_appointment_no(appointment_obj)
                    appointment_obj.save()
                view_serializer = ConsumerViewSerializer(instance=consumer, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: view_serializer.data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/connect
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Connect
# Usage: Connect
# Tables used: ConsumerMaster
# Author: Rohan
# updated by : Chetan Dhongade
# Created on: 01-02-2021
# Updated date: 05-03-2021

class ConsumerConnect(GenericAPIView):

    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                consumer = get_consumer_by_id_string(request.data['consumer_id'])
                consumer_service_contract_detail_obj = get_consumer_service_contract_detail_by_id_string(
                    request.data['consumer_service_contract_detail_id'])
                if consumer_service_contract_detail_obj:
                    service_contract_obj = get_utility_service_contract_master_by_id(
                        consumer_service_contract_detail_obj.service_contract_id)
                    if service_contract_obj:
                        utility_product_obj = get_utility_product_by_id(service_contract_obj.utility_product_id)


                work_order_type_obj = get_work_order_type_by_key('CONNECTION')
                work_order_sub_type_obj = get_work_order_sub_type_by_key('CONNECTION')

                utility_work_order_type_obj = UtilityWorkOrderType.objects.get(work_order_type_id=work_order_type_obj.id)
                utility_work_order_sub_type_obj = UtilityWorkOrderSubType.objects.get(work_order_sub_type_id=work_order_sub_type_obj.id)


                work_order_master_obj = WorkOrderMaster.objects.get(utility_product_id=utility_product_obj.id,
                                            utility_work_order_type_id= utility_work_order_type_obj.id,
                                            utility_work_order_sub_type_id = utility_work_order_sub_type_obj.id
                                            )

                request.data['work_order_master_id'] = str(work_order_master_obj.id_string)

                try:
                    previous_connection_request = ServiceAppointmentTbl.objects.filter(
                        Q(consumer_service_contract_detail_id=consumer_service_contract_detail_obj.id)
                        & Q(is_active=False) &
                        Q(Q(work_order_master_id=work_order_master_obj.id)) &
                        ~Q(state_id=7) &
                        Q(state_id=1))
                    if previous_connection_request:
                        raise CustomAPIException(
                            "Service Appointment Already Exist",
                            status_code=status.HTTP_409_CONFLICT)
                except Exception as e:
                    res = self.handle_exception(e)
                    return Response({
                        STATE: EXCEPTION,
                        RESULT: str(e),
                    }, status=res.status_code)

                appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                if appointment_serializer.is_valid(raise_exception=True):
                    appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                    appointment_obj.utility = consumer.utility
                    appointment_obj.sa_number = generate_service_appointment_no(appointment_obj)
                    appointment_obj.save()
                # view_serializer = ConsumerViewSerializer(instance=consumer, context={'request': request})

                # return the service appointent  obj to print the recipt in the front end
                view_serializer = ServiceAppointmentSerializer(instance=appointment_obj, context={'request': request})

                return Response({
                    STATE: SUCCESS,
                    RESULT: view_serializer.data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/consumer/disconnect
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: disconnect
# Usage: disconnect
# Tables used: ConsumerMaster
# Author: Rohan
# updated by : Chetan Dhongade
# Created on: 01-02-2021
# Updated date: 05-03-2021
class ConsumerDisconnect(GenericAPIView):
    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                consumer_service_contract_detail_obj = get_consumer_service_contract_detail_by_id_string(
                    request.data['consumer_service_contract_detail_id'])

                if consumer_service_contract_detail_obj:
                    service_contract_obj = get_utility_service_contract_master_by_id(
                        consumer_service_contract_detail_obj.service_contract_id)
                    if service_contract_obj:
                        utility_product_obj = get_utility_product_by_id(service_contract_obj.utility_product_id)

                work_order_type_obj = get_work_order_type_by_key('DISCONNECTION')

                if work_order_type_obj:
                    utility_work_order_type_obj = get_utility_work_order_type_by_id(work_order_type_obj.id)

                # check disconnect type is TEMPORARY OR PERMANENT
                if request.data['disconnect_type'] == 'TEMPORARY':
                    work_order_sub_type_obj = get_work_order_sub_type_by_key('TEMPORARY_DISCONNECTION')
                if request.data['disconnect_type'] == 'PERMANENT':
                    work_order_sub_type_obj = get_work_order_sub_type_by_key('PERMANENT_DISCONNECTION')

                if work_order_sub_type_obj:
                    utility_work_order_sub_type_obj = get_utility_work_order_sub_type_by_id(work_order_sub_type_obj.id)
                if utility_product_obj and utility_work_order_type_obj and utility_work_order_sub_type_obj:
                    work_order_master_obj = WorkOrderMaster.objects.get(
                        utility_work_order_type_id= utility_work_order_type_obj.id,
                        utility_work_order_sub_type_id=utility_work_order_sub_type_obj.id,
                        utility_product_id=utility_product_obj.id)

                request.data['work_order_master_id'] = str(work_order_master_obj.id_string)

                # prevent adding multiple request for the same meter
                try:
                    previous_work_order_master_obj = WorkOrderMaster.objects.filter(
                        utility_work_order_type_id=utility_work_order_type_obj.id,
                        utility_product_id=utility_product_obj.id)
                    disconnection_id = []
                    for i in previous_work_order_master_obj:
                        disconnection_id.append(i.id)

                    previous_connection_request = ServiceAppointmentTbl.objects.filter(
                        Q(consumer_service_contract_detail_id=consumer_service_contract_detail_obj.id)
                        & Q(is_active=False) &
                        Q(work_order_master_id__in=disconnection_id)&
                        ~Q(state_id=7) &
                        Q(state_id=1))
                    if previous_connection_request:
                        raise CustomAPIException(
                            "Service Appointment Already Exist",
                            status_code=status.HTTP_409_CONFLICT)
                except Exception as e:
                    res = self.handle_exception(e)
                    return Response({
                        STATE: EXCEPTION,
                        RESULT: str(e),
                    }, status=res.status_code)

                appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                if appointment_serializer.is_valid(raise_exception=True):
                    appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                    appointment_obj.utility = consumer_service_contract_detail_obj.utility
                    appointment_obj.sa_number = generate_service_appointment_no(appointment_obj)
                    appointment_obj.save()

                # view_serializer = ConsumerServiceContractDetailViewSerializer(instance=consumer_service_contract_detail_obj, context={'request': request})

                # serializer to return the created servie appointment for printing the recipt

                view_serializer = ServiceAppointmentSerializer(instance=appointment_obj, context={'request': request})

                return Response({
                    STATE: SUCCESS,
                    RESULT: view_serializer.data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)



# API Header
# API end Point: api/v1/consumer/outage
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Outage
# Usage: Outage 
# Tables used: workorder master, service appointment 
# Author: Chetan
# Created on: 09-03-2021
class ConsumerOutage(GenericAPIView):
    @is_token_validate
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                consumer_service_contract_detail_obj = get_consumer_service_contract_detail_by_id_string(
                    request.data['consumer_service_contract_detail_id'])
                work_order_master_obj = get_work_order_master_by_id_string(request.data['work_order_master_id'])
                try:
                    previous_connection_request = ServiceAppointmentTbl.objects.filter(
                        Q(consumer_service_contract_detail_id=consumer_service_contract_detail_obj.id)
                        & Q(is_active=False) &
                        Q(work_order_master_id=work_order_master_obj.id)&
                        ~Q(state_id=7) &
                        Q(state_id=1))
                    if previous_connection_request:
                        raise CustomAPIException(
                            "Service Appointment Already Exist",
                            status_code=status.HTTP_409_CONFLICT)
                except Exception as e:
                    res = self.handle_exception(e)
                    return Response({
                        STATE: EXCEPTION,
                        RESULT: str(e),
                    }, status=res.status_code)

                appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                if appointment_serializer.is_valid(raise_exception=True):
                    appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                    appointment_obj.utility = consumer_service_contract_detail_obj.utility
                    appointment_obj.is_active = False
                    appointment_obj.save()

                view_serializer = ServiceAppointmentSerializer(instance=appointment_obj, context={'request': request})
                return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                    }, status=status.HTTP_200_OK)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

# API Header
# API end Point: api/v1/consumer/service
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Service 
# Usage: service 
# Tables used: workorder master, service appointment 
# Author: Chetan Dhongade 
# Created on: 09-03-2021
class ConsumerService(GenericAPIView):
    @is_token_validate
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                consumer_service_contract_detail_obj = get_consumer_service_contract_detail_by_id_string(
                    request.data['consumer_service_contract_detail_id'])
                work_order_master_obj = get_work_order_master_by_id_string(request.data['work_order_master_id'])
                try:
                    previous_connection_request = ServiceAppointmentTbl.objects.filter(
                        Q(consumer_service_contract_detail_id=consumer_service_contract_detail_obj.id)
                        & Q(is_active=False) &
                        Q(work_order_master_id=work_order_master_obj.id)&
                        ~Q(state_id=7) &
                        Q(state_id=1))
                    if previous_connection_request:
                        raise CustomAPIException(
                            "Service Appointment Already Exist",
                            status_code=status.HTTP_409_CONFLICT)
                except Exception as e:
                    res = self.handle_exception(e)
                    return Response({
                        STATE: EXCEPTION,
                        RESULT: str(e),
                    }, status=res.status_code)

                appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                if appointment_serializer.is_valid(raise_exception=True):
                    appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                    appointment_obj.utility = consumer_service_contract_detail_obj.utility
                    appointment_obj.is_active = False
                    appointment_obj.save()

                view_serializer = ServiceAppointmentSerializer(instance=appointment_obj, context={'request': request})
                return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                    }, status=status.HTTP_200_OK)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)
            
            


#consumer transfer 
#Auther: Chetan Dhongade 
class ConsumerTransfer(GenericAPIView):
    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                consumer_service_contract_detail_obj = get_consumer_service_contract_detail_by_id_string(
                    request.data['consumer_service_contract_detail_id'])

                if consumer_service_contract_detail_obj:
                    service_contract_obj = get_utility_service_contract_master_by_id(
                        consumer_service_contract_detail_obj.service_contract_id)
                    if service_contract_obj:
                        utility_product_obj = get_utility_product_by_id(service_contract_obj.utility_product_id)

                work_order_type_obj = get_work_order_type_by_key('TRANSFER')

                if work_order_type_obj:
                    utility_work_order_type_obj = get_utility_work_order_type_by_id(work_order_type_obj.id)

                
                #create the transfer connection request 
                
                work_order_sub_type_connect_obj = get_work_order_sub_type_by_key('TRANSFER_CONNECT')
    
                if work_order_sub_type_connect_obj:
                    utility_work_order_sub_type_connect_obj = get_utility_work_order_sub_type_by_id(work_order_sub_type_connect_obj.id)
                   
                    
                if utility_product_obj and utility_work_order_type_obj and utility_work_order_sub_type_connect_obj:
                    work_order_master_obj = WorkOrderMaster.objects.get(
                        utility_work_order_type_id= utility_work_order_type_obj.id,
                        utility_work_order_sub_type_id=utility_work_order_sub_type_connect_obj.id,
                        utility_product_id=utility_product_obj.id)

                request.data['work_order_master_id'] = str(work_order_master_obj.id_string)

                # prevent adding multiple request for the same meter
                try:
                    previous_work_order_master_obj = WorkOrderMaster.objects.filter(
                        utility_work_order_type_id=utility_work_order_type_obj.id,
                        utility_product_id=utility_product_obj.id)
                    transfer_id = []
                    for i in previous_work_order_master_obj:
                        transfer_id.append(i.id)

                    previous_transfer_request = ServiceAppointmentTbl.objects.filter(
                        Q(consumer_service_contract_detail_id=consumer_service_contract_detail_obj.id)
                        & Q(is_active=False) &
                        Q(work_order_master_id__in=transfer_id)&
                        ~Q(state_id=7) &
                        Q(state_id=1))
                    if previous_transfer_request:
                        raise CustomAPIException(
                            "Transfer Request Already Exist",
                            status_code=status.HTTP_409_CONFLICT)
                except Exception as e:
                    res = self.handle_exception(e)
                    return Response({
                        STATE: EXCEPTION,
                        RESULT: str(e),
                    }, status=res.status_code)

                appointment_serializer = ServiceAppointmentSerializer(data=request.data)
                if appointment_serializer.is_valid(raise_exception=True):
                    appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                    appointment_obj.utility = consumer_service_contract_detail_obj.utility
                    appointment_obj.consumer_service_contract_detail_id = consumer_service_contract_detail_obj.id
                    appointment_obj.is_active = False
                    appointment_obj.save()

                #making the transfer disconnection request 
                work_order_sub_type_disconnect_obj = get_work_order_sub_type_by_key('TRANSFER_DISCONNECT')
                if work_order_sub_type_disconnect_obj:
                    utility_work_order_sub_type_disconnect_obj = get_utility_work_order_sub_type_by_id(work_order_sub_type_disconnect_obj.id)
                if utility_product_obj and utility_work_order_type_obj and utility_work_order_sub_type_disconnect_obj:
                    work_order_master_obj = WorkOrderMaster.objects.get(
                        utility_work_order_type_id= utility_work_order_type_obj.id,
                        utility_work_order_sub_type_id=utility_work_order_sub_type_disconnect_obj.id,
                        utility_product_id=utility_product_obj.id)
                request.data['custom_data']['work_order_master_id'] = str(work_order_master_obj.id_string)
                appointment_serializer = ServiceAppointmentSerializer(data=request.data['custom_data'])
                if appointment_serializer.is_valid(raise_exception=True):
                    appointment_obj = appointment_serializer.create(appointment_serializer.validated_data, user)
                    appointment_obj.utility = consumer_service_contract_detail_obj.utility
                    appointment_obj.consumer_service_contract_detail_id = consumer_service_contract_detail_obj.id
                    appointment_obj.is_active = False
                    appointment_obj.save()

                view_serializer = ServiceAppointmentSerializer(instance=appointment_obj, context={'request': request})

                return Response({
                    STATE: SUCCESS,
                    RESULT: view_serializer.data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)