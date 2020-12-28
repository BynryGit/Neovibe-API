from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.contract.models.contract_type import ContractType as ContractTypeTbl, get_contract_type_by_id_string
from v1.contract.serializers.contract_type import ContractTypeViewSerializer, ContractTypeSerializer, ContractTypeListSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from rest_framework.generics import GenericAPIView
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import CONTRACT_TYPE_NOT_FOUND, STATE, SUCCESS, EXCEPTION, RESULT, ERROR
from rest_framework.response import Response
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from django.db import transaction
from api.constants import ADMIN, UTILITY_MASTER, EDIT
from v1.commonapp.views.custom_exception import CustomAPIException

# API Header
# API end Point: api/v1/contract/:id_string/type/list
# API verb: GET
# Package: Basic
# Modules: Contract
# Sub Module: Type
# Interaction: Get contract type list
# Usage: API will fetch required data for contract type list.
# Tables used: 2.12.70 Contract Type
# Author: Gaurav
# Created on: 09/11/2020

class ContractTypeList(generics.ListAPIView):
    try:
        serializer_class = ContractTypeListSerializer
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
                    queryset = ContractTypeTbl.objects.filter(utility=utility,is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(CONTRACT_TYPE_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')

# API Header
# API end Point: api/v1/contract/:id_string/type
# API verb: GET,PUT
# Package: Basic
# Modules: Contract
# Sub Module: Type
# Interaction: Get single contract, Update single contract
# Usage: View, Update.
# Tables used: 2.12.70 Contract Type
# Author: Gaurav
# Created on: 09/11/2020 


class ContractTypeDetail(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            contract = get_contract_type_by_id_string(id_string)
            if contract:
                serializer = ContractTypeViewSerializer(instance=contract, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: CONTRACT_TYPE_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            contract_type_obj = get_contract_type_by_id_string(id_string)
            if contract_type_obj:
                serializer = ContractTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    contract_type_obj = serializer.update(contract_type_obj, serializer.validated_data, user)
                    view_serializer = ContractTypeViewSerializer(instance=contract_type_obj,
                                                                 context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: CONTRACT_TYPE_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            con = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=con.status_code)

# API Header
# API end Point: api/v1/contract/type
# API verb: POST
# Package: Basic
# Modules: Contract
# Sub Module: Type
# Interaction: Add contract type 
# Usage: API will Add contract type.
# Tables used: 2.12.70 Contract Type
# Author: Gaurav
# Created on: 09/11/2020

class ContractType(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = ContractTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                contract_obj = serializer.create(serializer.validated_data, user)
                view_serializer = ContractTypeViewSerializer(instance=contract_obj, context={'request': request})
                return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                        STATE: ERROR,
                        RESULT: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)