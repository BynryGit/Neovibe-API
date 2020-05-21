__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS, DUPLICATE
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.supplier.serializers.supplier import SupplierViewSerializer, SupplierSerializer
from v1.userapp.models.user_master import UserDetail
from v1.supplier.models.supplier import Supplier as SupplierTbl, get_supplier_by_id_string


# API Header
# API end Point: api/v1/supplier/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Supplier list
# Usage: API will fetch required data for supplier list against filter and search
# Tables used: Supplier
# Author: Akshay
# Created on: 21/05/2020

class SupplierList(generics.ListAPIView):
    try:
        serializer_class = SupplierViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant__id_string',)
        ordering = ('name',) # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    queryset = SupplierTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/supplier
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create Supplier object
# Usage: API will create suplier object based on valid data
# Tables used: Supplier
# Author: Akshay
# Created on: 21/05/2020

class Supplier(GenericAPIView):
    serializer_class = SupplierSerializer

    def post(self, request):
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

                    duplicate_supplier_obj = SupplierTbl.objects.filter(utility__id_string=request.data['utility'], name=request.data['name'])
                    if duplicate_supplier_obj:
                        return Response({
                            STATE: DUPLICATE,
                        }, status=status.HTTP_404_NOT_FOUND)
                    else:
                        serializer = SupplierSerializer(data=request.data)
                        if serializer.is_valid():
                            supplier_obj = serializer.create(serializer.validated_data, user)
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: {'supplier_id_string': supplier_obj.id_string},
                            }, status=status.HTTP_201_CREATED)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
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
# API end Point: api/v1/supplier/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View Supplier object
# Usage: API will fetch and edit required data for Supplier using id_string
# Tables used: Supplier
# Author: Akshay
# Created on: 21/05/2020

class SupplierDetail(GenericAPIView):
    serializer_class = SupplierSerializer

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

                    supplier_obj = get_supplier_by_id_string(id_string)
                    if supplier_obj:
                        serializer = SupplierViewSerializer(instance=supplier_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: serializer.data,
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

                    supplier_obj = get_supplier_by_id_string(id_string)
                    if supplier_obj:
                        serializer = SupplierSerializer(data=request.data)
                        if serializer.is_valid():
                            supplier_obj = serializer.update(supplier_obj, serializer.validated_data, user)
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: {'supplier_id_string': supplier_obj.id_string},
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
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