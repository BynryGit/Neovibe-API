from rest_framework import generics, status
import traceback
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.payment.models.payment_type import PaymentType as PaymentTypeModel, get_payment_type_by_id_string
from v1.payment.serializer.payment_type import PaymentTypeListSerializer, PaymentTypeViewSerializer, \
    PaymentTypeSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from api.constants import *
from v1.commonapp.views.pagination import StandardResultsSetPagination


# API Header
# API end Point: api/v1/payment/:id_string/type/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Payment Type list
# Usage: API will fetch all Payment Type list
# Tables used: Payment Type Table
# Author: Chinmay
# Created on: 03/12/2020


class PaymentTypeList(generics.ListAPIView):
    try:
        serializer_class = PaymentTypeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    # utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = PaymentTypeModel.objects.all()
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("PaymentType not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/Payment/Type
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: PaymentType Post
# Usage: API will POST PaymentType into database
# Tables used: PaymentType
# Author: Chinmay
# Created on: 09/11/2020
class PaymentType(GenericAPIView):

    @is_token_validate
    # @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        global payment_type_total
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            if "payment_details" in request.data:
                payment_type_total = request.data.pop('payment_details')
            for payment in payment_type_total:
                a = get_payment_type_by_id_string(id_string=payment['id_string'])
                serializer = PaymentTypeSerializer(data=request.data)
                request.data['payment_type_id'] = a.id
                request.data['name'] = a.name
                if serializer.is_valid(raise_exception=False):
                    print("INSIDE IFFF",serializer.validated_data)
                    payment_type_obj = serializer.create(serializer.validated_data, user)
                    print("Payment Type Obj",payment_type_obj)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            view_serializer = PaymentTypeViewSerializer(instance=payment_type_obj, context={'request': request})
            return Response({
                STATE: SUCCESS,
                RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/payment/type/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: PaymentTypes corresponding to the id
# Usage: API will fetch and update PaymentType for a given id
# Tables used: PaymentType
# Author: Chinmay
# Created on: 09/11/2020


class PaymentTypeDetail(GenericAPIView):

    @is_token_validate
    # @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            PaymentType = get_payment_type_by_id_string(id_string)
            if PaymentType:
                serializer = PaymentTypeViewSerializer(instance=PaymentType, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

    @is_token_validate
    # @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            payment_type_obj = get_payment_type_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = payment_type_obj.name
            if payment_type_obj:
                serializer = PaymentTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    payment_type_obj = serializer.update(payment_type_obj, serializer.validated_data, user)
                    view_serializer = PaymentTypeViewSerializer(instance=payment_type_obj,
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
