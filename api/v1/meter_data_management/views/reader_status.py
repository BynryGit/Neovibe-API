from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from django.db import transaction
from master.models import get_user_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.models.meter_status import get_meter_status_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.userapp.decorators import is_token_validate, role_required
from v1.meter_data_management.serializers.reader_status import ReaderStatusViewSerializer, ReaderStatusSerializer, \
    ReaderStatusListSerializer
from v1.meter_data_management.models.reader_status import ReaderStatus as ReaderStatusModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.meter_data_management.models.reader_status import get_reader_status_by_id_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.custom_filter_backend import CustomFilter
from api.messages import READER_STATUS_NOT_FOUND, SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from api.constants import *


# API Header
# API end Point: api/v1/utility/:id_string/reader_status/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Reader Status list
# Usage: API will fetch all Read Cycle list
# Tables used: ReaderStatus
# Author: Chinmay
# Created on: 3/3/2021


class ReaderStatusList(generics.ListAPIView):
    try:
        serializer_class = ReaderStatusListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'meter_status_id')
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    self.request.query_params._mutable = True
                    if 'meter_status_id' in self.request.query_params:
                        self.request.query_params['meter_status_id'] = get_meter_status_by_id_string(
                            self.request.query_params['meter_status_id']).id
                    self.request.query_params._mutable = False
                    queryset = ReaderStatusModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(READER_STATUS_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/meter-data/reader-status
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Reader Status post
# Usage: API will Post the Reader Status
# Tables used: ReaderStatus
# Author: Chinmay
# Created on: 3/3/2021


class ReaderStatus(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                serializer = ReaderStatusSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    reader_status_obj = serializer.create(serializer.validated_data, user)
                    view_serializer = ReaderStatusViewSerializer(instance=reader_status_obj, context={'request': request})
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
# API end Point: api/v1/meter-data/reader-status/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Reader Status corresponding to the id
# Usage: API will fetch and update Reader Status for a given id
# Tables used: ReaderStatus
# Author: Chinmay
# Created on: 3/3/2021


class ReaderStatusDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            reader_status = get_reader_status_by_id_string(id_string)
            if reader_status:
                serializer = ReaderStatusViewSerializer(instance=reader_status, context={'request': request})
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
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            reader_status_obj = get_reader_status_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = reader_status_obj.name
            if reader_status_obj:
                serializer = ReaderStatusSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    reader_status_obj = serializer.update(reader_status_obj, serializer.validated_data, user)
                    view_serializer = ReaderStatusViewSerializer(instance=reader_status_obj,
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
