from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.survey.models.survey_type import SurveyType as SurveyTypeModel,get_survey_type_by_id_string
from v1.survey.serializers.survey_type import SurveyTypeListSerializer,SurveyTypeViewSerializer,SurveyTypeSerializer
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, get_payload, is_authorized
from rest_framework.response import Response
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from v1.commonapp.views.logger import logger
from master.models import get_user_by_id_string
from api.messages import *
from api.constants import *

# API Header
# API end Point: api/v1/survey/utility/:id_string/survey_type/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Survey Type list
# Usage: API will fetch all State list
# Tables used: Survey Type
# Author: Chinmay
# Created on: 28/11/2020

class SurveyTypeList(generics.ListAPIView):
    try:
        serializer_class = SurveyTypeListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = SurveyTypeModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Survey Type not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')

# API Header
# API end Point: api/v1/survey/survey_type
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Survey post
# Usage: API will Post the Surveys
# Tables used: Survey Type
# Author: Chinmay
# Created on: 28/11/2020
class SurveyType(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = SurveyTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                survey_type_obj = serializer.create(serializer.validated_data, user)
                view_serializer = SurveyTypeViewSerializer(instance=survey_type_obj, context={'request': request})
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
# API end Point: api/v1/survey/survey_type/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Survey Type corresponding to the id
# Usage: API will fetch and update Survey Types for a given id
# Tables used: Survey Types
# Author: Chinmay
# Created on: 28/11/2020


class SurveyTypeDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            survey_type = get_survey_type_by_id_string(id_string)
            if survey_type:
                serializer = SurveyTypeViewSerializer(instance=survey_type, context={'request': request})
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
            survey_type_obj = get_survey_type_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = survey_type_obj.name
            if survey_type_obj:
                serializer = SurveyTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    survey_type_obj = serializer.update(survey_type_obj, serializer.validated_data, user)
                    view_serializer = SurveyTypeViewSerializer(instance=survey_type_obj,
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
        
