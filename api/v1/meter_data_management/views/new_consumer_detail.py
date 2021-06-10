__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.constants import MX, VALIDATION, EDIT, VIEW
from master.models import get_user_by_id_string
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.new_consumer_detail import NewConsumerDetail as NewConsumerDetailTbl, \
    get_new_consumer_detail_by_id_string
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id_string
from v1.meter_data_management.serializers.new_consumer_detail import NewConsumerDetailViewSerializer, \
    NewConsumerDetailSerializer
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, DATA_NOT_PROVIDED, CONSUMER_NOT_FOUND
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException


# API Header
# API end Point: api/v1/meter-data/new-consumer/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: schedule list
# Usage: API will fetch required data for new consumer list against filter and search
# Tables used: New Consumer Details
# Author: Akshay
# Created on: 07/06/2021

class NewConsumerDetailList(generics.ListAPIView):
    try:
        serializer_class = NewConsumerDetailViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'schedule_log_id',)
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',) # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    self.request.query_params._mutable = True
                    if 'schedule_log_id' in self.request.query_params:
                        self.request.query_params['schedule_log_id'] = get_schedule_log_by_id_string(
                            self.request.query_params['schedule_log_id']).id
                    self.request.query_params._mutable = False
                    queryset = NewConsumerDetailTbl.objects.filter(is_confirmed=False, is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='MX', sub_module='METER_READING')
        raise APIException


# API Header
# API end Point: api/v1/meter-data/new-consumer
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create new consumer object
# Usage: API will create new consumer object based on valid data
# Tables used: New Consumer Details
# Author: Akshay
# Created on: 07/06/2021

class NewConsumerDetail(GenericAPIView):
    @is_token_validate
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            dict = {}
            if len(request.data) > 0:
                dict['image_missing'] = []
                dict['create_new_consumer'] = []
                dict['create_new_consumer_error'] = []
                dict['serializer_error'] = []
                image_dict = {}
                for data in request.data:
                    meter_image = data.get("meter_image")
                    # if meter_image:
                    new_consumer_serializer = NewConsumerDetailSerializer(data=data)
                    if new_consumer_serializer.is_valid():
                        new_consumer_obj = new_consumer_serializer.create(new_consumer_serializer.validated_data,
                                                                          user)
                        if new_consumer_obj:
                            dict['create_new_consumer'].append(data.get('consumer_no'))
                            # image_dict[meter_reading_obj.id] = {}
                            # image_dict[meter_reading_obj.id]['meter_image'] = json.dumps(meter_image)
                        else:
                            dict['create_new_consumer_error'].append(data.get('consumer_no'))
                    else:
                        dict['serializer_error'].append(data.get('consumer_no'))
                    # else:
                    #     dict['image_missing'].append(data.get('consumer_no'))
                return Response({
                    STATE: SUCCESS,
                    RESULT: dict,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: SUCCESS,
                    RESULT: DATA_NOT_PROVIDED,
                }, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='METER_READING')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/new-consumer/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View New Consumer object
# Usage: API will fetch and edit required data for New Consumer using id_string
# Tables used: New Consumer Details
# Author: Akshay
# Created on: 09/06/2021

class NewConsumerDetailView(GenericAPIView):
    @is_token_validate
    @role_required(MX, VALIDATION, VIEW)
    def get(self, request, id_string):
        try:
            new_consumer_obj = get_new_consumer_detail_by_id_string(id_string)
            if new_consumer_obj:
                new_consumer_serializer = NewConsumerDetailViewSerializer(instance=new_consumer_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: new_consumer_serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: CONSUMER_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='SCHEDULE')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(MX, VALIDATION, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            new_consumer_obj = get_new_consumer_detail_by_id_string(id_string)
            if new_consumer_obj:
                new_consumer_serializer = NewConsumerDetailSerializer(data=request.data)
                if new_consumer_serializer.is_valid():
                    new_consumer_obj = new_consumer_serializer.update(new_consumer_obj, new_consumer_serializer.validated_data, user)
                    schedule_view_serializer = NewConsumerDetailViewSerializer(instance=new_consumer_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: schedule_view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: new_consumer_serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: CONSUMER_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='MX', sub_module='SCHEDULE')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
