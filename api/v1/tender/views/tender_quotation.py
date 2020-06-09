__author__ = "aki"

import traceback
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DUPLICATE, RESULT, DATA_ALREADY_EXISTS
from master.models import User
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, \
    ObjectNotFoundException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tender.models.tender import get_tender_by_id_string
from v1.tender.models.tender_quotation import TenderQuotation as TenderQuotationTbl, get_tender_quotation_by_id_string
from v1.tender.serializers.tender_quotation import TenderQuotationViewSerializer, TenderQuotationSerializer


# API Header
# API end Point: api/v1/tender/id_string/quotation/list
# API verb: GET
# Package: Basic
# Modules: Tender
# Sub Module: Quotation
# Interaction: Get tender quotation list
# Usage: API will fetch required data for tender quotation list.
# Tables used: 2.7.5 Tender Quotation
# Author: Akshay
# Created on: 09/06/2020


class TenderQuotationList(generics.ListAPIView):
    try:
        serializer_class = TenderQuotationViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('tenant__name', 'utility__name')
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name', 'utility__name',)

        def get_queryset(self):
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    tender_obj = get_tender_by_id_string(self.kwargs['id_string'])
                    if tender_obj:
                        queryset = TenderQuotationTbl.objects.filter(tender_id=tender_obj.id, is_active=True)
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
# API end Point: api/v1/tender/id_string/quotation
# API verb: POST
# Package: Basic
# Modules: Tender
# Sub Module: Quotation
# Interaction: Create tender quotation
# Usage: API will create tender quotation object based on valid data
# Tables used: 2.7.5 Tender Quotation
# Author: Akshay
# Created on: 09/06/2020

class TenderQuotation(GenericAPIView):
    serializer_class = TenderQuotationSerializer

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
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end
                    tender_obj = get_tender_by_id_string(id_string)
                    if tender_obj:
                        serializer = TenderQuotationSerializer(data=request.data)
                        if serializer.is_valid():
                            tender_quotation_obj = serializer.create(serializer.validated_data, tender_obj, user)
                            if tender_quotation_obj:
                                serializer = TenderQuotationViewSerializer(tender_quotation_obj, context={'request': request})
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
# API end Point: api/v1/tender/quotation/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Tender
# Sub Module: Quotation
# Interaction: For edit and get single tender quotation
# Usage: API will edit and get tender quotation
# Tables used: 2.7.5 Tender Quotation
# Author: Akshay
# Created on: 09/06/2020

class TenderQuotationDetail(GenericAPIView):
    serializer_class = TenderQuotationSerializer

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

                    tender_quotation_obj = get_tender_quotation_by_id_string(id_string)
                    if tender_quotation_obj:
                        serializer = TenderQuotationViewSerializer(tender_quotation_obj, context={'request': request})
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

                    tender_quotation_obj = get_tender_quotation_by_id_string(id_string)
                    if tender_quotation_obj:
                        serializer = TenderQuotationSerializer(data=request.data)
                        if serializer.is_valid():
                            tender_quotation_obj = serializer.update(tender_quotation_obj, serializer.validated_data, user)
                            serializer = TenderQuotationViewSerializer(tender_quotation_obj, context={'request': request})
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