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
from v1.payment.models.payment_sub_type import PaymentSubType as PaymentSubTypeModel, get_payment_sub_type_by_id_string
from v1.payment.serializer.payment_sub_type import PaymentSubTypeListSerializer,PaymentSubTypeSerializer,PaymentSubTypeViewSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from api.constants import *
from v1.commonapp.views.custom_filter_backend import CustomFilter
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.payment.models.payment_type import get_payment_type_by_id_string

# API Header
# API end Point: api/v1/payment/:id_string/subtype/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Payment SubType list
# Usage: API will fetch all Payment SubType list
# Tables used: Payment SubType Table
# Author: Chinmay
# Created on: 03/12/2020


class PaymentSubTypeList(generics.ListAPIView):
    try:
        serializer_class = PaymentSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    if 'TYPE' in self.request.query_params:
                        payment_type_obj = get_payment_type_by_id_string(self.request.query_params['TYPE'])
                        queryset = PaymentSubTypeModel.objects.filter(payment_type_id = payment_type_obj.id)
                    else:
                        # utility = get_utility_by_id_string(self.kwargs['id_string'])
                        queryset = PaymentSubTypeModel.objects.all()
                        queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("PaymentSubType not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/Payment/SubType
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: PaymentSubType Post
# Usage: API will POST PaymentSubType into database
# Tables used: PaymentSubType
# Author: Chinmay
# Created on: 09/11/2020
class PaymentSubType(GenericAPIView):

    @is_token_validate
    # @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = PaymentSubTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                PaymentSubType_obj = serializer.create(serializer.validated_data, user)
                view_serializer = PaymentSubTypeViewSerializer(instance=PaymentSubType_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

# API Header
# API end Point: api/v1/payment/subtype/:id_string/
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: PaymentSubTypes corresponding to the id
# Usage: API will fetch and update PaymentSubType for a given id
# Tables used: PaymentSubType
# Author: Chinmay
# Created on: 09/11/2020


class PaymentSubTypeDetail(GenericAPIView):

    @is_token_validate
    # @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            PaymentSubType = get_payment_sub_type_by_id_string(id_string)
            if PaymentSubType:
                serializer = PaymentSubTypeViewSerializer(instance=PaymentSubType, context={'request': request})
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
            PaymentSubType_obj = get_payment_sub_type_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = PaymentSubType_obj.name
            if PaymentSubType_obj:
                serializer = PaymentSubTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    PaymentSubType_obj = serializer.update(PaymentSubType_obj, serializer.validated_data, user)
                    view_serializer = PaymentSubTypeViewSerializer(instance=PaymentSubType_obj,
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