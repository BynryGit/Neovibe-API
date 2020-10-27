__author__ = "aki"

import traceback
from api.constants import *
from django.db import transaction
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from master.models import User, get_user_by_id_string
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DUPLICATE, DATA_ALREADY_EXISTS, RESULT
from v1.commonapp.models.module import get_module_by_id
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_master import UtilityMaster as UtilityMasterTbl, get_utility_by_id_string
from v1.utility.serializers.utility import UtilityMasterViewSerializer, UtilityMasterSerializer
from v1.utility.serializers.utility_module import UtilityModuleSerializer
from v1.utility.serializers.utility_sub_module import UtilitySubModuleSerializer


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
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'ERROR')
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
    # @is_token_validate
    # @role_required(ADMIN, UTILITY, EDIT)
    def post(self, request):
        print('------------')
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                if 'utility_module_submodule' in request.data:
                    utility_module_submodule = request.data.pop('utility_module_submodule')
                serializer = UtilityMasterSerializer(data=request.data)
                if serializer.is_valid():
                    utility_obj = serializer.create(serializer.validated_data, user)
                    if utility_obj:
                        if utility_module_submodule:
                            for utility_mod_sub in utility_module_submodule:
                                utility_module = utility_mod_sub['utility_module']
                                utility_module['tenant'] = utility_obj.tenant.id_string
                                utility_module['utility'] = utility_obj.id_string
                                utility_module_serializer = UtilityModuleSerializer(data=utility_module)
                                if utility_module_serializer.is_valid():
                                    utility_module_obj = utility_module_serializer.create(utility_module_serializer.validated_data, user)
                                    if utility_module_obj:
                                        for submodule in utility_mod_sub['utility_submodule']:
                                            utility_submodule = submodule
                                            utility_submodule['tenant'] = utility_obj.tenant.id_string
                                            utility_submodule['utility'] = utility_obj.id_string
                                            module_obj = get_module_by_id(utility_module_obj.module_id)
                                            utility_submodule['module_id'] = module_obj.id_string
                                            utility_submodule_serializer = UtilitySubModuleSerializer(data=utility_submodule)
                                            if utility_submodule_serializer.is_valid():
                                                utility_submodule_obj = utility_submodule_serializer.create(utility_submodule_serializer.validated_data, user)
                                            else:
                                                return Response({
                                                    STATE: ERROR,
                                                    RESULT: utility_submodule_serializer.errors,
                                                }, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        return Response({
                                            STATE: DUPLICATE,
                                            RESULT: DATA_ALREADY_EXISTS,
                                        }, status=status.HTTP_409_CONFLICT)
                                else:
                                    return Response({
                                        STATE: ERROR,
                                        RESULT: utility_module_serializer.errors,
                                    }, status=status.HTTP_400_BAD_REQUEST)
                        serializer = UtilityMasterViewSerializer(instance=utility_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: serializer.data,
                        }, status=status.HTTP_201_CREATED)
                    else:
                        return Response({
                            STATE: DUPLICATE,
                            RESULT: DATA_ALREADY_EXISTS,
                        }, status=status.HTTP_409_CONFLICT)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    serializer_class = UtilityMasterSerializer

    def get(self, request, id_string):
        try:
            # Checking authentication start
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end
                
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
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    utility_obj = get_utility_by_id_string(id_string)
                    if utility_obj:
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
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)