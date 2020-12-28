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
from v1.payment.models.payment_mode import PaymentMode as PaymentModeModel, get_payment_mode_by_id_string
from v1.payment.serializer.payment_mode import PaymentModeListSerializer,PaymentModeSerializer,PaymentModeViewSerializer
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
# API end Point: api/v1/payment/:id_string/mode/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Payment Mode list
# Usage: API will fetch all Payment Mode list
# Tables used: Payment Mode Table
# Author: Chinmay
# Created on: 03/12/2020


class PaymentModeList(generics.ListAPIView):
    try:
        serializer_class = PaymentModeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    # utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = PaymentModeModel.objects.all()
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("PaymentMode not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/Payment/mode
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: PaymentMode Post
# Usage: API will POST PaymentMode into database
# Tables used: PaymentMode
# Author: Chinmay
# Created on: 09/11/2020
class PaymentMode(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = PaymentModeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                PaymentMode_obj = serializer.create(serializer.validated_data, user)
                view_serializer = PaymentModeViewSerializer(instance=PaymentMode_obj, context={'request': request})
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
# API end Point: api/v1/payment/mode/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: PaymentModes corresponding to the id
# Usage: API will fetch and update PaymentMode for a given id
# Tables used: PaymentMode
# Author: Chinmay
# Created on: 09/11/2020


class PaymentModeDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            PaymentMode = get_payment_mode_by_id_string(id_string)
            if PaymentMode:
                serializer = PaymentModeViewSerializer(instance=PaymentMode, context={'request': request})
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
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            PaymentMode_obj = get_payment_mode_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = PaymentMode_obj.name
            if PaymentMode_obj:
                serializer = PaymentModeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    PaymentMode_obj = serializer.update(PaymentMode_obj, serializer.validated_data, user)
                    view_serializer = PaymentModeViewSerializer(instance=PaymentMode_obj,
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