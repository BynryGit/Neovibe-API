__author__ = "aki"

import traceback
from api.constants import *
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.views.logger import logger
from v1.utility.models.utility_services_number_format import \
    get_utility_service_number_format_by_utility_id_string_and_item
from v1.utility.serializers.numformat import UtilityServiceNumberFormatListSerializer, UtilityServiceNumberFormatSerializer, UtilityServiceNumberFormatViewSerializer
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat as UtilityNumberFormatTbl
from rest_framework import generics, status
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_master import get_utility_by_id_string
from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from django.db import transaction
from v1.utility.models.utility_services_number_format import get_utility_service_number_format_by_id_string, UtilityServiceNumberFormat



# API Header
# API end Point: api/v1/utility/id_string/numformat
# API verb: PUT
# Package: Basic
# Modules: Utility
# Sub Module: Numformat
# Tables used: 2.5.12 Notes
# Author: Chinmay
# Created on: 23/11/2020


class UtilityNumformatDetail(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            numformat_obj = get_utility_service_number_format_by_id_string(id_string)
            if numformat_obj:
                serializer = UtilityServiceNumberFormatSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    numformat_obj = serializer.update(numformat_obj, serializer.validated_data, user)
                    view_serializer = UtilityServiceNumberFormatViewSerializer(instance=numformat_obj,
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
    

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            numformat = get_utility_service_number_format_by_id_string(id_string)
            if numformat:
                serializer = UtilityServiceNumberFormatViewSerializer(instance=numformat, context={'request': request})
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


# API Header
# API end Point: api/v1/utility/:id_string/num_format/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Num Format list
# Usage: API will fetch all Num Format list
# Tables used: UtilityServiceNumFormat
# Author: Chinmay
# Created on: 23/11/2020

class UtilityNumFormatList(generics.ListAPIView):
    try:
        serializer_class = UtilityServiceNumberFormatListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityNumberFormatTbl.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Num Format not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


class UtilityNumFormat(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = UtilityServiceNumberFormatSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                numformat_obj = serializer.create(serializer.validated_data, user)
                view_serializer = UtilityServiceNumberFormatViewSerializer(instance=numformat_obj, context={'request': request})
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
