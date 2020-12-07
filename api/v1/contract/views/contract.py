__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, DUPLICATE, DATA_ALREADY_EXISTS
from master.models import User
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.contract.serializers.contract import ContractViewSerializer, ContractSerializer, ContractListSerializer
from v1.contract.models.contract import Contract as ContractTbl, get_contract_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string


# API Header
# API end Point: api/v1/contract/list
# API verb: GET
# Package: Basic
# Modules: Contract
# Sub Module: Contract
# Interaction: Get contract list
# Usage: API will fetch required data for contract list.
# Tables used: Contract
# Author: Akshay
# Created on: 28/05/2020


# class ContractList(generics.ListAPIView):
#     try:
#         serializer_class = ContractViewSerializer
#         pagination_class = StandardResultsSetPagination

#         filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
#         filter_fields = ('name', 'tenant__id_string', 'utility__id_string')
#         ordering_fields = ('name', 'tenant__name', 'utility__name')
#         ordering = ('name',)  # always give by default alphabetical order
#         search_fields = ('name',)

#         def get_queryset(self):
#             if is_token_valid(self.request.headers['token']):
#                 if is_authorized(1,1,1,1):
#                     queryset = ContractTbl.objects.filter(is_active=True)
#                     return queryset
#                 else:
#                     raise InvalidAuthorizationException
#             else:
#                 raise InvalidTokenException
#     except Exception as ex:
#         logger().log(ex, 'ERROR')
#         raise APIException



class ContractList(generics.ListAPIView):
    try:
        serializer_class = ContractListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('id_string',)
        ordering_fields = ('name',)
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name')

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ContractTbl.objects.filter(utility=utility,is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/contract/
# API verb: POST
# Package: Basic
# Modules: Contract
# Sub Module: Contract
# Interaction: Create contract
# Usage: API will create contract object based on valid data
# Tables used: Contract
# Author: Akshay
# Created on: 28/05/2020

class Contract(GenericAPIView):
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
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    serializer = ContractSerializer(data=request.data)
                    if serializer.is_valid():
                        contract_obj = serializer.create(serializer.validated_data, user)
                        if contract_obj:
                            serializer = ContractViewSerializer(contract_obj, context={'request': request})
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
# API end Point: api/v1/contract/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Contract
# Sub Module: Contract
# Interaction: For edit and get single contract
# Usage: API will edit and get contract
# Tables used: Contract
# Author: Akshay
# Created on: 28/05/2020

class ContractDetail(GenericAPIView):
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

                    contract_obj = get_contract_by_id_string(id_string)
                    if contract_obj:
                        serializer = ContractViewSerializer(contract_obj, context={'request': request})
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
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    contract_obj = get_contract_by_id_string(id_string)
                    if contract_obj:
                        serializer = ContractSerializer(data=request.data)
                        if serializer.is_valid():
                            contract_obj = serializer.update(contract_obj, serializer.validated_data, user)
                            serializer = ContractViewSerializer(contract_obj, context={'request': request})
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