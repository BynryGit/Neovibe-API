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
from v1.commonapp.models.department_subtype import DepartmentSubtype as DepartmentSubtypeTbl, get_department_subtype_by_id_string
from v1.commonapp.serializers.department_subtype import DepartmentSubTypeViewSerializer, DepartmentSubTypeSerializer, DepartmentSubTypeListSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination


class DepartmentSubTypeList(generics.ListAPIView):
    try:
        serializer_class = DepartmentSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    # utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = DepartmentSubtypeTbl.objects.all()
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Department SubType not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/dept_subtype
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Department SubType Post
# Usage: API will POST Department SubType into database
# Tables used: Department SubType
# Author: Chinmay
# Created on: 09/11/2020
class DepartmentSubType(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = DepartmentSubTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                dept_subtype_obj = serializer.create(serializer.validated_data, user)
                view_serializer = DepartmentSubTypeViewSerializer(instance=dept_subtype_obj, context={'request': request})
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
# API end Point: api/v1/:id_string/dept_subtype
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: dept_subtypes corresponding to the id
# Usage: API will fetch and update dept types for a given id
# Tables used: Department SubTypes
# Author: Chinmay
# Created on: 09/11/2020


class DepartmentSubTypeDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            department = get_department_subtype_by_id_string(id_string)
            if department:
                serializer = DepartmentSubTypeViewSerializer(instance=department, context={'request': request})
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
            subtype_obj = get_department_subtype_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = subtype_obj.name
            if subtype_obj:
                serializer = DepartmentSubTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    subtype_obj = serializer.update(subtype_obj, serializer.validated_data, user)
                    view_serializer = DepartmentSubTypeViewSerializer(instance=subtype_obj,
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