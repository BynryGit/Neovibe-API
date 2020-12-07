from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.supplier.models.supplier_type import SupplierType as SupplierTypeTbl, get_supplier_type_by_id_string
from v1.supplier.serializers.supplier_type import SupplierTypeListSerializer, SupplierTypeViewSerializer, SupplierTypeSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from rest_framework.generics import GenericAPIView
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import SUPPLIER_TYPE_NOT_FOUND, STATE, SUCCESS, EXCEPTION, RESULT, ERROR
from rest_framework.response import Response
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from django.db import transaction
from api.constants import ADMIN, UTILITY, EDIT
from v1.commonapp.views.custom_exception import CustomAPIException


# API Header
# API end Point: api/v1/supplier/id_string/type/list
# API verb: GET
# Package: Basic
# Modules: Supplier
# Sub Module: Supplier Type
# Interaction: Get supplier Type list
# Usage: API will fetch required data for supplier type list.
# Tables used: SupplierType
# Author: Gaurav
# Created on: 23/11/2020

class SupplierTypeList(generics.ListAPIView):
    try:
        serializer_class = SupplierTypeListSerializer
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
                    queryset = SupplierTypeTbl.objects.filter(utility=utility,is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(SUPPLIER_TYPE_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/supplier/id_string/type
# API verb: GET,PUT
# Package: Basic
# Modules: Supplier
# Sub Module: Supplier Type
# Interaction: For edit and get single supplier type
# Usage: API will edit and get supplier type
# Tables used: SupplierType
# Author: Gaurav
# Created on: 23/11/2020

class SupplierTypeDetail(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY, EDIT)
    def get(self, request, id_string):
        try:
            supplier = get_supplier_type_by_id_string(id_string)
            if supplier:
                serializer = SupplierTypeViewSerializer(instance=supplier, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: SUPPLIER_TYPE_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, UTILITY, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            supplier_type_obj = get_supplier_type_by_id_string(id_string)
            if supplier_type_obj:
                serializer = SupplierTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    supplier_type_obj = serializer.update(supplier_type_obj, serializer.validated_data, user)
                    view_serializer = SupplierTypeViewSerializer(instance=supplier_type_obj,
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
                    RESULT: SUPPLIER_TYPE_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            con = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=con.status_code)


# API Header
# API end Point: api/v1/supplier/type
# API verb: POST
# Package: Basic
# Modules: Supplier
# Sub Module: Supplier Type
# Interaction: Create supplier type
# Usage: API will create supplier type object based on valid data
# Tables used: SupplierType
# Author: Gaurav
# Created on: 23/11/2020

class SupplierType(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = SupplierTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                supplier_obj = serializer.create(serializer.validated_data, user)
                view_serializer = SupplierTypeViewSerializer(instance=supplier_obj, context={'request': request})
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
