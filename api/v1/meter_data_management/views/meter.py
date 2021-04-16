__author__ = "aki"

import xlrd
from django.db import transaction
from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from api.messages import STATE, ERROR, EXCEPTION, SUCCESS, RESULT, METER_NOT_FOUND, SUCCESSFULLY_DATA_SAVE
from api.constants import MX, EDIT, METER_MASTER, VIEW
from master.models import get_user_by_id_string
from v1.commonapp.models.global_lookup import get_global_lookup_by_value
from v1.commonapp.models.lifecycle import LifeCycle as LifeCycleTbl
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.notes import Notes as NoteTbl
from v1.commonapp.models.premises import get_premise_by_name
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.serializers.lifecycle import LifeCycleListSerializer
from v1.commonapp.serializers.note import NoteListSerializer, NoteSerializer, NoteViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.meter_data_management.models.meter_make import get_meter_make_by_name
from v1.meter_data_management.models.route import get_route_by_name
from v1.meter_data_management.views.status import check_meter_status
from v1.userapp.decorators import is_token_validate, role_required
from v1.meter_data_management.models.meter import Meter as MeterTbl, get_meter_by_id_string
from v1.meter_data_management.serializers.meter import MeterViewSerializer, MeterSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_name
from v1.commonapp.views.custom_filter_backend import CustomFilter

# API Header
# API end Point: api/v1/meter-data/meter/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter list
# Usage: API will fetch required data for meter list against filter and search
# Tables used: Meter
# Author: Akshay
# Created on: 13/02/2021


class MeterList(generics.ListAPIView):
    try:
        serializer_class = MeterViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string',)
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    queryset = MeterTbl.objects.filter(is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='MX', sub_module='METER_MASTER')
        raise APIException


# API Header
# API end Point: api/v1/meter
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create meter object
# Usage: API will create meter object based on valid data
# Tables used: Meter
# Author: Akshay
# Created on: 13/02/2021

class Meter(GenericAPIView):
    @is_token_validate
    @role_required(MX, METER_MASTER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                meter_values = []
                utility_obj = get_utility_by_id_string(request.data['utility_id_string'])
                meter_file = request.FILES["meter_file"]
                workbook = xlrd.open_workbook(file_contents=meter_file.read())

                number_of_rows = workbook.sheets()[0].nrows
                number_of_columns = workbook.sheets()[0].ncols

                for row in range(1, number_of_rows):
                    row_values = []
                    for col in range(number_of_columns):
                        value = (workbook.sheets()[0].cell(row, col).value)
                        row_values.append(value)
                    meter_values.append(row_values)

                for value in meter_values:
                    if MeterTbl.objects.filter(tenant=user.tenant, utility=utility_obj,
                                               meter_no=value[5], is_active=True).exists():
                        pass
                    else:
                        route_obj = get_route_by_name(name=value[0]).id
                        premise_obj = get_premise_by_name(value[1]).id
                        utility_product_obj = get_utility_product_by_name(value[2]).id
                        meter_type_obj = get_global_lookup_by_value(value[3]).id
                        meter_status = check_meter_status(value[4])
                        meter_make_obj = get_meter_make_by_name(value[7]).id
                        MeterTbl(
                            tenant=user.tenant,
                            utility=utility_obj,
                            route_id=route_obj,
                            premise_id=premise_obj,
                            utility_product_id=utility_product_obj,
                            meter_type_id=meter_type_obj,
                            meter_status=meter_status,
                            meter_no=value[5],
                            meter_digit=value[6],
                            meter_make_id=meter_make_obj,
                            current_reading=value[8],
                            latitude=value[9],
                            longitude=value[10],
                            install_date=value[11]
                        ).save()
                return Response({
                    STATE: SUCCESS,
                    RESULT: SUCCESSFULLY_DATA_SAVE,
                }, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='METER_MASTER')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/meter/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View Edit Meter object
# Usage: API will fetch and edit required data for meter using id_string
# Tables used: Meter
# Author: Akshay
# Created on: 13/02/2021

class MeterDetail(GenericAPIView):
    @is_token_validate
    @role_required(MX, METER_MASTER, VIEW)
    def get(self, request, id_string):
        try:
            meter_obj = get_meter_by_id_string(id_string)
            if meter_obj:
                serializer = MeterViewSerializer(instance=meter_obj, context={'request': request})
                meter_serializer = serializer.data
                next_record = MeterTbl.objects.filter(id__gt=meter_obj.id).exclude(id=meter_obj.id).order_by('id').first()
                previous_record = MeterTbl.objects.filter(id__lt=meter_obj.id).exclude(id=meter_obj.id).order_by('-id').first()
                if next_record:
                    meter_serializer['Next_Record'] = next_record.id_string
                else:
                    meter_serializer['Next_Record'] = next_record
                if previous_record:
                    meter_serializer['Previous_Record'] = previous_record.id_string
                else:
                    meter_serializer['Previous_Record'] = previous_record
                return Response({
                    STATE: SUCCESS,
                    RESULT: meter_serializer,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: METER_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='METER_MASTER')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(MX, METER_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            meter_obj = get_meter_by_id_string(id_string)
            if meter_obj:
                meter_serializer = MeterSerializer(data=request.data)
                if meter_serializer.is_valid():
                    meter_obj = meter_serializer.update(meter_obj, meter_serializer.validated_data, user)
                    meter_view_serializer = MeterViewSerializer(instance=meter_obj,
                                                                      context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: meter_view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: meter_serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: METER_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='METER_MASTER')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/meter/life-cycle/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter life cycle list
# Usage: API will fetch required data for meter life cycle list against filter and search
# Tables used: LifeCycle
# Author: Akshay
# Created on: 16/02/2021

class MeterLifeCycleList(generics.ListAPIView):
    try:
        serializer_class = LifeCycleListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'object_id')
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',)  # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1, 1, 1, user_obj):
                    self.request.query_params._mutable = True
                    module = get_module_by_key("CONSUMER_OPS")
                    sub_module = get_sub_module_by_key("METER_DATA")
                    if 'object_id' in self.request.query_params:
                        self.request.query_params['object_id'] = get_meter_by_id_string(self.request.query_params['object_id']).id
                    self.request.query_params._mutable = False
                    queryset = LifeCycleTbl.objects.filter(module_id=module, sub_module_id=sub_module, is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='MX', sub_module='METER_MASTER')
        raise APIException


# API Header
# API end Point: api/v1/meter/note/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: meter note list
# Usage: API will fetch required data for meter note list against filter and search
# Tables used: Notes
# Author: Akshay
# Created on: 17/02/2021

class MeterNoteList(generics.ListAPIView):
    try:
        serializer_class = NoteListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'identification_id')
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',)  # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1, 1, 1, user_obj):
                    self.request.query_params._mutable = True
                    if 'identification_id' in self.request.query_params:
                        self.request.query_params['identification_id'] = \
                            get_meter_by_id_string(self.request.query_params['identification_id']).id
                    self.request.query_params._mutable = False
                    queryset = NoteTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='MX', sub_module='METER_MASTER')
        raise APIException


# API Header
# API end Point: api/v1/meter/:id_string/note
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create meter note object
# Usage: API will create meter not object based on valid data
# Tables used: Notes
# Author: Akshay
# Created on: 17/02/2021

# todo need to fix this api and note serializer
class MeterNoteDetail(GenericAPIView):
    @is_token_validate
    @role_required(MX, METER_MASTER, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            meter_obj = get_meter_by_id_string(id_string)
            module = get_module_by_key("CONSUMER_OPS")
            sub_module = get_sub_module_by_key("METER_DATA")
            note_serializer = NoteSerializer(data=request.data)
            if note_serializer.is_valid():
                meter_note_obj = note_serializer.create(note_serializer.validated_data, user)
                meter_note_obj.identification_id = meter_obj.id
                meter_note_obj.tenant = meter_obj.tenant
                meter_note_obj.utility = meter_obj.utility
                meter_note_obj.module_id = module
                meter_note_obj.sub_module_id = sub_module
                meter_note_obj.save()
                note_view_serializer = NoteViewSerializer(instance=meter_note_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: note_view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: note_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(ex)
            logger().log(ex, 'MEDIUM', module='MX', sub_module='METER_MASTER')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
