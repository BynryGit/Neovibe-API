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
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.consumer.models.consumer_category import ConsumerCategory
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.models.consumer_ownership import ConsumerOwnership
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_sub_category import ConsumerSubCategory
from v1.consumer.serializers.consumer import ConsumerSerializer, ConsumerViewSerializer
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_ownership import ConsumerOwnershipListSerializer
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.models.consumer_payment import get_payments_by_consumer_no, get_payment_by_id_string
from v1.payment.serializer.payment import *
from v1.service.models.consumer_services import get_consumer_services_by_consumer_no
from v1.service.serializers.service import ServiceDetailListSerializer
from v1.userapp.decorators import is_token_validate, role_required

# API Header
# API end Point: api/v1/consumer
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Add
# Usage: Add
# Tables used: ConsumerMaster
# Auther: Rohan
# Created on: 19/05/2020
from v1.utility.models.utility_master import get_utility_by_id_string


class Consumer(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            serializer = ConsumerSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                consumer_obj = serializer.create(serializer.validated_data, user)
                view_serializer = ConsumerViewSerializer(instance=consumer_obj, context={'request': request})
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
# API end Point: api/v1/consumer/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Get, Update
# Usage: Add
# Tables used: ConsumerMaster
# Auther: Rohan
# Created on: 19/05/2020
class ConsumerDetail(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, VIEW)
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
    @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            consumer = get_consumer_by_id_string(id_string)
            if consumer:
                serializer = ConsumerSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
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
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    consumer = get_consumer_by_id_string(self.kwargs['id_string'])
                    if consumer:
                        queryset = get_consumer_complaints_by_consumer_no(consumer.consumer_no)
                        return queryset
                    else:
                        raise InvalidAuthorizationException
                else:
                    raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'ERROR')
        raise APIException


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
# Tables used: CosumerComlaint
# Auther: Rohan
# Created on: 22/05/2020
class ConsumerComplaint(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, CONSUMER, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            consumer_obj = get_consumer_by_id_string(id_string)
            request.data['consumer_no'] = consumer_obj.consumer_no
            serializer = ComplaintSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                complaint = serializer.create(serializer.validated_data, user)
                view_serializer = ComplaintViewSerializer(instance=complaint, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
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
                if is_authorized(1,1,1,user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerCategory.objects.filter(utility = utility, is_active = True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer categories not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module = 'Consumer Ops', sub_module = 'Consumer')


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
                if is_authorized(1,1,1,user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerSubCategory.objects.filter(utility = utility, is_active = True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer sub categories not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module = 'Consumer Ops', sub_module = 'Consumer')


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
                if is_authorized(1,1,1,user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerOwnership.objects.filter(utility = utility, is_active = True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer ownership not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module = 'Consumer Ops', sub_module = 'Consumer')