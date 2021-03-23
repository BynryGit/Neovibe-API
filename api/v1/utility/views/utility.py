__author__ = "aki"

import traceback
from api.constants import *
from django.db import transaction
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_filter_backend import CustomFilter
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from master.models import get_user_by_id_string
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DUPLICATE, DATA_ALREADY_EXISTS, RESULT
from v1.commonapp.models.module import get_module_by_id
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_master import UtilityMaster as UtilityMasterTbl, get_utility_by_id_string, UTILITY_DICT
from v1.utility.serializers.utility import UtilityMasterViewSerializer, UtilityMasterSerializer
from v1.utility.serializers.utility_module import UtilityModuleSerializer, UtilityModuleViewSerializer
from v1.utility.serializers.utility_sub_module import UtilitySubModuleSerializer
from api.messages import *
from api.constants import *
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()

import boto3
from botocore.exceptions import NoCredentialsError
from rest_framework.parsers import FileUploadParser
from boto.s3.connection import S3Connection
from boto.s3.key import Key


# API Header
# API end Point: api/v1/utility/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Utility list
# Usage: API will fetch required data for utility list against filter and search
# Tables used: 2.1. Utility Master
# Author: Akshay
# Created on: 08/05/2020


class UtilityList(generics.ListAPIView):
    try:
        serializer_class = UtilityMasterViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        ordering = ('name',) # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = UtilityMasterTbl.objects.filter(is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY')
        raise APIException


# API Header
# API end Point: api/v1/:id_string/utility/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Utility list by tenant id_string
# Usage: API will fetch required data for utility list by tenant id_string
# Tables used: 2.1. Utility Master
# Author: Priyanka
# Created on: 08/05/2020


class UtilityListByTenant(generics.ListAPIView):
    try:
        serializer_class = UtilityMasterViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        ordering = ('name',) # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = UtilityMasterTbl.objects.filter(tenant__id_string=self.kwargs['id_string'],is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY')
        raise APIException


# API Header
# API end Point: api/v1/utility
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Create Utility object
# Usage: API will create utility object based on valid data
# Tables used: 2.1. Utility Master
# Author: Akshay
# Created on: 13/05/2020

class Utility(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = UtilityMasterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                area_obj = serializer.create(serializer.validated_data, user)
                area_obj.change_state(UTILITY_DICT["APPROVED"])
                view_serializer = UtilityMasterViewSerializer(instance=area_obj, context={'request': request})
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
# API end Point: api/v1/utility/id_string
# API verb: GET,PUT
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: View Utility object
# Usage: API will fetch and edit required data for utility using id_string
# Tables used: 2.1. Utility Master
# Author: Akshay
# Created on: 08/05/2020

class UtilityDetail(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            utility_obj = get_utility_by_id_string(id_string)
            if utility_obj:
                serializer = UtilityMasterViewSerializer(instance=utility_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            utility_obj = get_utility_by_id_string(id_string)
            if utility_obj:
                utility_obj.change_state(UTILITY_DICT["APPROVED"])
                serializer = UtilityMasterSerializer(data=request.data)
                if serializer.is_valid():
                    utility_obj = serializer.update(utility_obj, serializer.validated_data, user)
                    serializer = UtilityMasterViewSerializer(instance=utility_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UtilityModule(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            if 'utility_module_submodule' in request.data:
                utility_module_submodule = request.data.pop('utility_module_submodule')
                print(utility_module_submodule)
            for utility_mod_sub in utility_module_submodule:
                utility_module = utility_mod_sub['utility_module']
                print("Utility Module",utility_module)
                a = get_module_by_id_string(id_string=utility_module['module_id'])
                print("AAAA", a)
                serializer = UtilityModuleSerializer(data=request.data)
                request.data['module_id'] = a.id_string
                print("AAAAAAAID",a.id_string)
                request.data['label'] = a.name
                print("AAANAME",a.name)
                if serializer.is_valid(raise_exception=False):
                    print("validated", serializer.validated_data)
                    utility_module_obj = serializer.create(serializer.validated_data, user)
                    if utility_module_obj:
                        for submodule in utility_mod_sub['utility_submodule']:
                            utility_submodule = submodule
                            print("UUUUUU SSSSS",utility_submodule)
                            b = get_sub_module_by_id_string(id_string=utility_submodule['submodule_id'])
                            print("BBBBBBBBBBBBBB",b)
                            serializer = UtilitySubModuleSerializer(data = request.data)
                            print("Serializer",request.data)
                            request.data['submodule_id'] = b.id_string
                            print("BBBID",b.id_string)
                            request.data['label'] = b.name
                            print("bBBNAME",b.name)
                            request.data['module_id'] = a.id_string
                            print("Request Dta 222",request.data)
                            if serializer.is_valid(raise_exception=False):
                                print("SFjvcjh",serializer.validated_data)
                                utility_submodule_obj = serializer.create(serializer.validated_data, user)
                                print("VVVDSA",utility_submodule_obj)
                                # if utility_submodule_obj:
                                #     view_serializer = UtilitySubModuleSerializer(instance=utility_module_obj, context={'request': request})
                                #     return Response({
                                #         STATE: SUCCESS,
                                #         RESULTS: view_serializer.data,
                                #     }, status=status.HTTP_201_CREATED)
                                # else:
                                #     return Response({
                                #         STATE: ERROR,
                                #         RESULTS: list(serializer.errors.values())[0][0],
                                #     }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            view_serializer = UtilityModuleViewSerializer(instance=utility_module_obj, context={'request': request})
            return Response({
                STATE: SUCCESS,
                RESULTS: view_serializer.data,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


