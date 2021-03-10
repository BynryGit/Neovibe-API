__author__ = "aki"

import traceback
from api.constants import *
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from v1.userapp.decorators import is_token_validate, role_required
from master.models import get_user_by_id_string
from v1.commonapp.views.custom_filter_backend import CustomFilter
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_sub_module import get_utility_submodule_by_id_string, UtilitySubModule as UtilitySubModuleTbl
from v1.utility.serializers.utility_sub_module import UtilitySubModuleViewSerializer, UtilitySubModuleSerializer
from v1.utility.models.utility_module import get_utility_module_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.utility.serializers.utility_sub_module import UtilitySubModuleListSerializer
from v1.commonapp.models.sub_module import SubModule as SubModuleTbl
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_master import get_utility_by_id_string
from rest_framework.decorators import api_view


# API Header
# API end Point: api/v1/utility/id_string/submodule/list
# API verb: GET
# Package: Basic
# Modules: Utility
# Sub Module: SubModule
# Interaction: Utility Submodule list
# Usage: API will fetch utility submodule list against single utility
# Tables used: 2.4 Utility SubModule
# Author: Akshay
# Created on: 12/05/2020


class UtilitySubModuleList(generics.ListAPIView):
    try:
        serializer_class = UtilitySubModuleViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('tenant__name', 'utility__name')
        ordering = ('utility__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name', 'utility__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = UtilitySubModuleTbl.objects.filter(utility__id_string=self.kwargs['id_string'], is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/SUBMODULE')
        raise APIException


# API Header
# API end Point: api/v1/utility/module/id_string/submodule/list
# API verb: GET
# Package: Basic
# Modules: utility
# Sub Module: SubModule
# Interaction: utility Submodule list by module is_string
# Usage: API will fetch utility submodule list against single module
# Tables used: 2.3 utility SubModule
# Author: Akshay
# Created on: 14/10/2020


class UtilitySubModuleListByModule(generics.ListAPIView):
    try:
        serializer_class = UtilitySubModuleViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    utility_module_obj = get_utility_module_by_id_string(self.kwargs['id_string'])
                    if utility_module_obj:
                        queryset = UtilitySubModuleTbl.objects.filter(module_id=utility_module_obj.id, is_active=True)
                        return queryset
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/SUBMODULE')
        raise APIException


# API Header
# API end Point: api/v1/utility/submodule/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Utility
# Sub Module: SubModule
# Interaction: For get and edit utility submodule
# Usage: API will fetch and edit utility submodule details
# Tables used: 2.4 Utility SubModule
# Author: Akshay
# Created on: 12/05/2020

class UtilitySubModuleDetail(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            utility_submodule_obj = get_utility_submodule_by_id_string(id_string)
            if utility_submodule_obj:
                serializer = UtilitySubModuleViewSerializer(utility_submodule_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/SUBMODULE')
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
            utility_submodule_obj = get_utility_submodule_by_id_string(id_string)
            if utility_submodule_obj:
                serializer = UtilitySubModuleSerializer(data=request.data)
                if serializer.is_valid():
                    utility_submodule_obj = serializer.update(utility_submodule_obj, serializer.validated_data, user)
                    serializer = UtilitySubModuleViewSerializer(utility_submodule_obj,
                                                                context={'request': request})
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
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/SUBMODULE')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UtilitySubModuleListByUtility(generics.ListAPIView):
    try:
        serializer_class = UtilitySubModuleListSerializer
        pagination_class = StandardResultsSetPagination
        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilitySubModuleTbl.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Sub Module not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')  


@api_view(['DELETE'])
def api_delete_submodule(request,id_string):
    try:
        sub_module = get_utility_submodule_by_id_string(id_string)
    except:
        return Response(status=status.status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        print(sub_module)
        operation = sub_module.delete()
        data = {}
        if operation:
            data["success"] = "Delete Successful"
        else:
            data["failure"] = "Delete Failed"
        
        return Response(data=data)
    
