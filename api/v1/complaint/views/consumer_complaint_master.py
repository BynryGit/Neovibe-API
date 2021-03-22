from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.complaint.models.consumer_complaint_master import ConsumerComplaintMaster as ConsumerComplaintMasterModel, get_consumer_complaint_master_by_id_string
from v1.complaint.serializers.consumer_complaint_master import ConsumerComplaintMasterListSerializer, \
    ConsumerComplaintMasterViewSerializer, ConsumerComplaintMasterSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import *
from api.constants import *


class ConsumerComplaintMasterList(generics.ListAPIView):
    try:
        serializer_class = ConsumerComplaintMasterListSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    if 'consumer_service_contract_detail_id_string' in self.request.query_params:
                        consumer_service_contract_detail_obj = get_consumer_service_contract_detail_by_id_string(self.request.query_params['consumer_service_contract_detail_id_string'])
                        utility_service_contract_master_obj = get_utility_service_contract_master_by_id(consumer_service_contract_detail_obj.service_contract_id)
                        utility_product_id = utility_service_contract_master_obj.utility_product_id
                        queryset = ConsumerComplaintMasterModel.objects.filter(utility=utility, is_active=True, utility_product_id=utility_product_id)
                    else:
                        queryset = ConsumerComplaintMasterModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer Complaint master not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Complaint', sub_module='Complaint')


# API Header
# API end Point: api/v1/utility/complaint-master
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Complaint Master post
# Usage: API will Post the Complaint Master
# Tables used: Complaint Master
# Author: Chinmay
# Created on: 11/2/2021
class ConsumerComplaintMaster(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = ConsumerComplaintMasterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                consumer_master_obj = serializer.create(serializer.validated_data, user)
                view_serializer = ConsumerComplaintMasterViewSerializer(instance=consumer_master_obj, context={'request': request})
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
# API end Point: api/v1/utility/state/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: City corresponding to the id
# Usage: API will fetch and update Cities for a given id
# Tables used: City
# Author: Chinmay
# Created on: 10/11/2020


class ConsumerComplaintMasterDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            city = get_consumer_complaint_master_by_id_string(id_string)
            if city:
                serializer = ConsumerComplaintMasterViewSerializer(instance=city, context={'request': request})
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
            consumer_master_obj = get_consumer_complaint_master_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = consumer_master_obj.name
            if consumer_master_obj:
                serializer = ConsumerComplaintMasterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    consumer_master_obj = serializer.update(consumer_master_obj, serializer.validated_data, user)
                    view_serializer = ConsumerComplaintMasterViewSerializer(instance=consumer_master_obj,
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
