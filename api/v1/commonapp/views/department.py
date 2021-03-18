import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from v1.commonapp.views.logger import logger
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from rest_framework.exceptions import APIException
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import *
from api.constants import *
from api.messages import *
from v1.commonapp.models.department import Department as DepartmentTbl, get_department_by_tenant_id_string, \
    get_department_by_id_string
from v1.commonapp.serializers.department import DepartmentSerializer, DepartmentViewSerializer, DepartmentListSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination


# API Header
# API end Point: api/v1/department/list
# API verb: GET
# Package: Basic
# Modules: Lookup
# Sub Module: Lookup
# Interaction: View Departments
# Usage: This will get the list of departments
# Tables used: Lookup - 2.12.16 Lookup - Department
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 12/05/2020


class DepartmentListByTenant(generics.ListAPIView):
    try:
        serializer_class = DepartmentSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('name', 'tenant__name', 'utility__name')
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name', 'utility__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    # queryset = DepartmentTbl.objects.filter(utility__id_string=self.kwargs['id_string'], is_active=True)
                    queryset = DepartmentTbl.objects.filter(tenant__id_string=self.kwargs['id_string'], is_active=True)

                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/departments/list
# API verb: GET
# Package: Basic
# Modules: Lookup
# Sub Module: Lookup
# Interaction: View Departments
# Usage: This will get the list of departments
# Tables used: Lookup - 2.12.16 Lookup - Department
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 12/05/2020


class DepartmentListByUtility(generics.ListAPIView):
    try:
        serializer_class = DepartmentSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('name', 'tenant__name', 'utility__name')
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name', 'utility__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    queryset = DepartmentTbl.objects.filter(utility__id_string=self.kwargs['id_string'], is_active=True)
                    # queryset = DepartmentTbl.objects.filter(tenant__id_string=self.kwargs['id_string'], is_active=True)

                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/department
# API verb: GET
# Package: Basic
# Modules: Lookup
# Sub Module: Lookup
# Interaction: View Department
# Usage: This will get the detail of department
# Tables used: Lookup - 2.12.16 Lookup - Department
# Author: Arpita
# Created on: 12/05/2020


class Department(GenericAPIView):

    def get(self, request, id_string):
        try:
            department = get_department_by_id_string(id_string)
            if department:
                serializer = DepartmentViewSerializer(instance=department, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentTypeList(generics.ListAPIView):
    try:
        serializer_class = DepartmentListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    # utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = DepartmentTbl.objects.all()
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Department Type not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/dept_type
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Department Type Post
# Usage: API will POST Department Type into database
# Tables used: Department Type
# Author: Chinmay
# Created on: 09/11/2020
class DepartmentType(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = DepartmentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                dept_type_obj = serializer.create(serializer.validated_data, user)
                view_serializer = DepartmentViewSerializer(instance=dept_type_obj, context={'request': request})
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
# API end Point: api/v1/:id_string/dept_type
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: dept_types corresponding to the id
# Usage: API will fetch and update dept types for a given id
# Tables used: Department Types
# Author: Chinmay
# Created on: 09/11/2020


class DepartmentTypeDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            department = get_department_by_id_string(id_string)
            if department:
                serializer = DepartmentViewSerializer(instance=department, context={'request': request})
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
            region_obj = get_department_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = region_obj.name
            if region_obj:
                serializer = DepartmentSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    region_obj = serializer.update(region_obj, serializer.validated_data, user)
                    view_serializer = DepartmentViewSerializer(instance=region_obj,
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
