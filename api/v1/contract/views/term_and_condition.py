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
from v1.contract.models.contract import get_contract_by_id_string
from v1.contract.serializers.term_and_condition import TermsAndConditionViewSerializer, TermsAndConditionSerializer
from v1.userapp.models.user_master import UserDetail
from v1.contract.models.terms_and_conditions import TermsAndCondition as TermsAndConditionTbl, \
    get_contract_term_and_condition_by_id_string


# API Header
# API end Point: api/v1/contract/id_string/t&c/list
# API verb: GET
# Package: Basic
# Modules: Contract
# Sub Module: T&C
# Interaction: Get contract t&c list
# Usage: API will fetch required data for contract t&c list.
# Tables used: 2.5.11 Terms & Conditions
# Author: Akshay
# Created on: 29/05/2020


class ContractTermAndConditionList(generics.ListAPIView):
    try:
        serializer_class = TermsAndConditionViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'terms_name',)
        ordering_fields = ('utility__id_string', 'terms')
        ordering = ('terms_name',)  # always give by default alphabetical order
        search_fields = ('terms_name', 'terms',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    contract_obj = get_contract_by_id_string(self.kwargs['id_string'])
                    if contract_obj:
                        queryset = TermsAndConditionTbl.objects.filter(contract=contract_obj.id, is_active=True)
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
# API end Point: api/v1/contract/id_string/t&c
# API verb: POST
# Package: Basic
# Modules: Contract
# Sub Module: T&C
# Interaction: Create contract t&c
# Usage: API will create contract t&c object based on valid data
# Tables used: 2.5.11 Terms & Conditions
# Author: Akshay
# Created on: 29/05/2020

class ContractTermAndCondition(GenericAPIView):
    serializer_class = TermsAndConditionSerializer

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
                    contract_obj = get_contract_by_id_string(id_string)
                    if contract_obj:
                        serializer = TermsAndConditionSerializer(data=request.data)
                        if serializer.is_valid():
                            contract_term_and_condition_obj = serializer.create(serializer.validated_data, contract_obj, user)
                            if contract_term_and_condition_obj:
                                serializer = TermsAndConditionViewSerializer(contract_term_and_condition_obj, context={'request': request})
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
# API end Point: api/v1/contract/t&c/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Contract
# Sub Module: T&C
# Interaction: For edit and get single contract t&c
# Usage: API will edit and get contract t&c
# Tables used: 2.5.11 Terms & Conditions
# Author: Akshay
# Created on: 29/05/2020

class ContractTermAndConditionDetail(GenericAPIView):
    serializer_class = TermsAndConditionSerializer

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

                    contract_term_and_condition_obj = get_contract_term_and_condition_by_id_string(id_string)
                    if contract_term_and_condition_obj:
                        serializer = TermsAndConditionViewSerializer(contract_term_and_condition_obj, context={'request': request})
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

                    contract_term_and_condition_obj = get_contract_term_and_condition_by_id_string(id_string)
                    if contract_term_and_condition_obj:
                        serializer = TermsAndConditionSerializer(data=request.data)
                        if serializer.is_valid():
                            contract_term_and_condition_obj = serializer.update(contract_term_and_condition_obj, serializer.validated_data, user)
                            serializer = TermsAndConditionViewSerializer(contract_term_and_condition_obj, context={'request': request})
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