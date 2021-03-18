from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.constants import *
from api.messages import *
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.userapp.decorators import is_token_validate
from v1.utility.models.utility_service_contract_master import \
    UtilityServiceContractMaster as UtilityServiceContractMasterModel, \
    get_utility_service_contract_master_by_id_string
from v1.utility.serializers.utility_service_contract_master import UtilityServiceContractMasterListSerializer, \
    UtilityServiceContractMasterDetailSerializer, UtilityServiceContractMasterViewSerializer, \
    UtilityServiceContractMasterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.utility.models.utility_master import get_utility_by_id_string


class UtilityServiceContractMasterList(generics.ListAPIView):
    try:
        serializer_class = UtilityServiceContractMasterListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityServiceContractMasterModel.objects.filter(utility=utility, is_active=True)
                    if 'consumer_sub_category_id' in self.request.query_params:
                        sub_category = get_consumer_sub_category_by_id_string(
                            self.request.query_params['consumer_sub_category_id'])
                        queryset = queryset.filter(consumer_sub_category_id=sub_category.id)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Utility service contracts not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Utility', sub_module='Utility')


# API Header
# API end Point: api/v1/utility/service_contract
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: City post
# Usage: API will Post the Service Contracts
# Tables used: UtilityServiceContractMaster
# Author: Chinmay
# Created on: 27/1/2021
class UtilityServiceContractMaster(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = UtilityServiceContractMasterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                contract_obj = serializer.create(serializer.validated_data, user)
                view_serializer = UtilityServiceContractMasterViewSerializer(instance=contract_obj,
                                                                             context={'request': request})
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
# API end Point: api/v1/utility/service_contract/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Service Contract corresponding to the id
# Usage: API will fetch and update Service Contracts for a given id
# Tables used: UtilityServiceContractMaster
# Author: Chinmay
# Created on: 27/1/2021


class UtilityServiceContractMasterDetail(GenericAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = UtilityServiceContractMasterDetailSerializer

    @is_token_validate
    # #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:

            contract = get_utility_service_contract_master_by_id_string(id_string)
            if contract:
                serializer = UtilityServiceContractMasterDetailSerializer(instance=contract,
                                                                          context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: UTILITY_SERVICE_CONTRACT_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Utility', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            contract_obj = get_utility_service_contract_master_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = contract_obj.name
            if contract_obj:
                serializer = UtilityServiceContractMasterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    contract_obj = serializer.update(contract_obj, serializer.validated_data, user)
                    view_serializer = UtilityServiceContractMasterViewSerializer(instance=contract_obj,
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
