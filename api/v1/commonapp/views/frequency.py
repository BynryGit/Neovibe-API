from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from v1.commonapp.models.frequency import Frequency, get_frequency_by_id_string
from v1.commonapp.serializers.frequency import FrequencySerializer,FrequencyViewSerializer,FrequencyListSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.models.frequency import Frequency as FrequencyModel
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from v1.commonapp.views.logger import logger
from v1.commonapp.models.frequency import get_frequency_by_id_string
from master.models import get_user_by_id_string
from api.messages import *
from api.constants import *


class FrequencyList(generics.ListAPIView):
    try:
        serializer_class = FrequencyListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = FrequencyModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Frequency not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/utility/frequency/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: States corresponding to the id
# Usage: API will fetch and update States for a given id
# Tables used: State
# Author: Chinmay
# Created on: 10/11/2020


class FrequencyDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            frequency = get_frequency_by_id_string(id_string)
            if frequency:
                serializer = FrequencyViewSerializer(instance=frequency, context={'request': request})
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
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            frequency_obj = get_frequency_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = frequency_obj.name
            if frequency_obj:
                serializer = FrequencySerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    frequency_obj = serializer.update(frequency_obj, serializer.validated_data, user)
                    view_serializer = FrequencyViewSerializer(instance=frequency_obj,
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

# API Header
# API end Point: api/v1/utility/state
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: State post
# Usage: API will Post the state
# Tables used: State
# Author: Chinmay
# Created on: 10/11/2020
class Frequency(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = FrequencySerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                frequency_obj = serializer.create(serializer.validated_data, user)
                view_serializer = FrequencyViewSerializer(instance=frequency_obj, context={'request': request})
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
    