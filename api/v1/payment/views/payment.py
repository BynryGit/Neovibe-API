from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.constants import *
from api.messages import *
from v1.commonapp.views.logger import logger
from v1.payment.models.consumer_payment import get_payment_by_id_string, PAYMENT_DICT, PAYMENT_TYPE_DICT
from v1.payment.serializer.payment import PaymentViewSerializer
from v1.registration.signals.signals import registration_payment_approved, registration_approved, after_payment
from v1.userapp.decorators import is_token_validate, role_required


# API Header
# API end Point: api/v1/payment/:id_string
# API verb: PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Payment
# Interaction: Approve payment
# Usage: View, Update
# Tables used: Payment
# Auther: Rohan
# Created on: 17/07/2020
class PaymentApprove(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, PAYMENT, EDIT)
    def put(self, request, id_string):
        try:
            payment = get_payment_by_id_string(id_string)
            if payment:
                with transaction.atomic():
                    payment.change_state(PAYMENT_DICT["APPROVED"])
                    # signal to registration start
                    if payment.type == PAYMENT_TYPE_DICT['REGISTRATION']:
                        registration_approved.connect(after_payment)
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
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Payments')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)


# API Header
# API end Point: api/v1/payment/:id_string
# API verb: PUT
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Payment
# Interaction: Reject payment
# Usage: View, Update
# Tables used: Payment
# Auther: Rohan
# Created on: 17/07/2020
class PaymentReject(GenericAPIView):

    @is_token_validate
    @role_required(CONSUMER_OPS, PAYMENT, EDIT)
    def put(self, request, id_string):
        try:
            payment = get_payment_by_id_string(id_string)
            if payment:
                with transaction.atomic():
                    # State change for payment start
                    if payment.type == PAYMENT_TYPE_DICT['REGISTRATION']:
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
            logger().log(e, 'HIGH', module='Consumer Ops', Sub_module='Payments')
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=status.HTTP_412_PRECONDITION_FAILED)