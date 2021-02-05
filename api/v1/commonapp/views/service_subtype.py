from v1.commonapp.serializers.service_request_sub_type import ServiceSubTypeListSerializer,ServiceSubTypeViewSerializer,ServiceSubTypeSerializer
from v1.commonapp.models.service_request_sub_type import ServiceSubTypes as ServiceSubTypeModel
from v1.commonapp.common_functions import is_token_valid,  is_authorized
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS,DUPLICATE,DATA_ALREADY_EXISTS
from v1.commonapp.serializers.region import TenantRegionSerializer
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import is_token_validate, role_required
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.serializers.region import TenantRegionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.models.service_request_sub_type import get_service_sub_type_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from api.messages import *
from api.constants import *
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException


# API Header
# API end Point: api/v1/service_subtype/list
# API verb: GET
# Package: Basic
# Modules: O&M
# Sub Module:
# Interaction: service_subtype List
# Usage: API will fetch required data for service_subtype list
# Tables used:  Service SubType
# Author: Priyanka Kachare
# Created on: 25/05/2020

# Api for getting Service Type  filter

class ServiceSubTypeList(generics.ListAPIView):
    try:
        serializer_class = ServiceSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'utility__id_string',)
        ordering_fields = ('name',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ServiceSubTypeModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Service SubType not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Work Order')

   


# API Header
# API end Point: api/v1/service_subtype/:id_string
# API verb: GET
# Package: Basic
# Modules: O&M
# Sub Module:
# Interaction: View service_subtype
# Usage: View
# Tables used: Service SubType
# Auther: Priyanka
# Created on: 25/05/2020

# API for view service_subtype details
class ServiceSubTypeDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            service_subtype = get_service_sub_type_by_id_string(id_string)
            if  service_subtype:
                serializer = ServiceSubTypeViewSerializer(instance= service_subtype, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Work Order')
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
            service_subtype_obj = get_service_sub_type_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = service_subtype_obj.name
            if service_subtype_obj:
                serializer = ServiceSubTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    service_subtype_obj = serializer.update(service_subtype_obj, serializer.validated_data, user)
                    view_serializer = ServiceSubTypeViewSerializer(instance=service_subtype_obj,
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
            logger().log(e, 'HIGH', module='Admin', sub_module='Work Order')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

# API Header
# API end Point: api/v1/service_subtype
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Service Type Post
# Usage: API will POST Service Type into database
# Tables used: Service Type
# Author: Chinmay
# Created on: 17/12/2020
class ServiceSubType(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = ServiceSubTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                service_subtype_obj = serializer.create(serializer.validated_data, user)
                view_serializer = ServiceSubTypeViewSerializer(instance=service_subtype_obj, context={'request': request})
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
            logger().log(e, 'HIGH', module='Admin', sub_module='Work Order')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)