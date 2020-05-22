__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS, DUPLICATE
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, \
    ObjectNotFoundException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.supplier.models.supplier import get_supplier_by_id_string
from v1.supplier.serializers.supplier_contract import ContractViewSerializer, ContractSerializer
from v1.userapp.models.user_master import UserDetail
from v1.contract.models.contracts import Contract as ContractTbl, get_contract_by_id_string


# API Header
# API end Point: api/v1/supplier/id_string/contract/list
# API verb: GET
# Package: Basic
# Modules: Supplier
# Sub Module: Contract
# Interaction: Get supplier contract list
# Usage: API will fetch required data for supplier contract list.
# Tables used: Contract
# Author: Akshay
# Created on: 22/05/2020


class SupplierContractList(generics.ListAPIView):
    try:
        serializer_class = ContractViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string', 'utility__id_string')
        ordering_fields = ('name', 'tenant__name', 'utility__name')
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    supplier_obj = get_supplier_by_id_string(self.kwargs['id_string'])
                    if supplier_obj:
                        queryset = ContractTbl.objects.filter(supplier=supplier_obj.id.id, is_active=True)
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
# API end Point: api/v1/supplier/id_string/contract
# API verb: POST
# Package: Basic
# Modules: Supplier
# Sub Module: Contract
# Interaction: Create supplier contract
# Usage: API will create supplier contract object based on valid data
# Tables used: Contract
# Author: Akshay
# Created on: 22/05/2020

class SupplierContract(GenericAPIView):
    serializer_class = ContractSerializer

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

                    duplicate_supplier_contract_obj = ContractTbl.objects.filter(utility__id_string=request.data['utility'], name=request.data['name'])
                    if duplicate_supplier_contract_obj:
                        return Response({
                            STATE: DUPLICATE,
                        }, status=status.HTTP_409_CONFLICT)
                    else:
                        serializer = ContractSerializer(data=request.data)
                        if serializer.is_valid():
                            supplier_contract_obj = serializer.create(serializer.validated_data, user)
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: {'supplier_contract_id_string': supplier_contract_obj.id_string},
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
# API end Point: api/v1/supplier/contract/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Supplier
# Sub Module: Contract
# Interaction: For edit and get single supplier contract
# Usage: API will edit and get supplier contract
# Tables used: Contract
# Author: Akshay
# Created on: 22/05/2020

class SupplierContractDetail(GenericAPIView):
    serializer_class = ContractSerializer

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

                    supplier_contract_obj = get_contract_by_id_string(id_string)
                    if supplier_contract_obj:
                        serializer = ContractViewSerializer(supplier_contract_obj, context={'request': request})
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

                    supplier_contract_obj = get_contract_by_id_string(id_string)
                    if supplier_contract_obj:
                        serializer = ContractSerializer(data=request.data)
                        if serializer.is_valid():
                            supplier_contract_obj = serializer.update(supplier_contract_obj, serializer.validated_data, user)
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: {'supplier_contract_id_string': supplier_contract_obj.id_string},
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