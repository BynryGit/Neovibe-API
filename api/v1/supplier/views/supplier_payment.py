__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DUPLICATE, RESULT, DATA_ALREADY_EXISTS
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, \
    ObjectNotFoundException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.supplier.models.supplier import get_supplier_by_id_string
from v1.supplier.serializers.supplier_payment import SupplierPaymentViewSerializer, SupplierPaymentSerializer
from v1.userapp.models.user_master import UserDetail
from v1.supplier.models.supplier_payment import SupplierPayment as SupplierPaymentTbl, get_supplier_payment_by_id_string


# API Header
# API end Point: api/v1/supplier/id_string/payment/list
# API verb: GET
# Package: Basic
# Modules: Supplier
# Sub Module: Payment
# Interaction: Get supplier payment list
# Usage: API will fetch required data for supplier payment list.
# Tables used: 2.5.10 SupplierPayment
# Author: Akshay
# Created on: 22/05/2020


class SupplierPaymentList(generics.ListAPIView):
    try:
        serializer_class = SupplierPaymentViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('tenant__name', 'utility__name')
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name', 'utility__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    supplier_obj = get_supplier_by_id_string(self.kwargs['id_string'])
                    if supplier_obj:
                        queryset = SupplierPaymentTbl.objects.filter(supplier=supplier_obj.id, is_active=True)
                        return queryset
                    else:
                        raise ObjectNotFoundException
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/supplier/id_string/payment
# API verb: POST
# Package: Basic
# Modules: Supplier
# Sub Module: Payment
# Interaction: Create supplier payment
# Usage: API will create supplier payment object based on valid data
# Tables used: 2.5.10 SupplierPayment
# Author: Akshay
# Created on: 22/05/2020

class SupplierPayment(GenericAPIView):
    serializer_class = SupplierPaymentSerializer

    def post(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = UserDetail.objects.get(id=2)
                    # Todo fetch user from request end
                    supplier_obj = get_supplier_by_id_string(id_string)
                    if supplier_obj:
                        serializer = SupplierPaymentSerializer(data=request.data)
                        if serializer.is_valid():
                            supplier_payment_obj = serializer.create(serializer.validated_data, supplier_obj, user)
                            if supplier_payment_obj:
                                serializer = SupplierPaymentViewSerializer(supplier_payment_obj,
                                                                           context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULT: serializer.data,
                                }, status=status.HTTP_201_CREATED)
                            else:
                                return Response({
                                    STATE: DUPLICATE,
                                    RESULT: DATA_ALREADY_EXISTS,
                                }, status=status.HTTP_409_CONFLICT)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULT: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/supplier/payment/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Supplier
# Sub Module: Payment
# Interaction: For edit and get single supplier payment
# Usage: API will edit and get supplier payment
# Tables used: 2.5.10 SupplierPayment
# Author: Akshay
# Created on: 22/05/2020

class SupplierPaymentDetail(GenericAPIView):
    serializer_class = SupplierPaymentSerializer

    def get(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end

                    supplier_payment_obj = get_supplier_payment_by_id_string(id_string)
                    if supplier_payment_obj:
                        serializer = SupplierPaymentViewSerializer(supplier_payment_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = UserDetail.objects.get(id=2)
                    # Todo fetch user from request end

                    supplier_payment_obj = get_supplier_payment_by_id_string(id_string)
                    if supplier_payment_obj:
                        serializer = SupplierPaymentSerializer(data=request.data)
                        if serializer.is_valid():
                            supplier_payment_obj = serializer.update(supplier_payment_obj, serializer.validated_data, user)
                            serializer = SupplierPaymentViewSerializer(supplier_payment_obj,
                                                                       context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULT: serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULT: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)