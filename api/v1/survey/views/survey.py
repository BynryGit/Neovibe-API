__author__ = "Priyanka"

from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
import traceback
from rest_framework.response import Response
from api.messages import SUCCESS,STATE,ERROR,EXCEPTION,DATA,RESULTS
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.survey.models.survey import get_survey_by_id_string,Survey as Surveytbl
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.survey.serializers.survey import SurveyViewSerializer,SurveyListSerializer,SurveySerializer
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.survey.views.common_functions import is_data_verified

# API Header
# API end Point: api/v1/survey/list
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Survey
# Interaction: Survey list
# Usage: API will fetch required data for Location and consumer Survey list
# Tables used: 2.3.1 Survey Master
# Author: Priyanka
# Created on: 28/04/2020


# API for getting list data of Location Survey
class SurveyList(generics.ListAPIView):
    try:
        serializer_class = SurveyListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'no_of_consumers',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            if is_token_valid(1):
                if is_authorized():
                    queryset = Surveytbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/survey
# API verb: POST
# Package: Basic
# Modules: S&M
# Sub Module: Survey
# Interaction: Add Survey
# Usage: Add
# Tables used:  2.3.6 Survey
# Auther: Priyanka
# Created on: 15/05/2020

class Survey(GenericAPIView):
    serializer_class = SurveySerializer

    def post(self, request):
        try:
            if is_token_valid(1):
                if is_authorized():
                    user = User.objects.get(id=2)
                    if is_data_verified(request):
                        serializer = SurveySerializer(data=request.data)
                        if serializer.is_valid():
                            survey_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = SurveyViewSerializer(instance=survey_obj,
                                                                         context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
                            }, status=status.HTTP_201_CREATED)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# API Header
# API end Point: api/v1/survey/:id_string
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module:  Survey
# Interaction: View  Survey
# Usage: View
# Tables used: 2.3.1 Survey Master
# Auther: Priyanka
# Created on: 29/04/2020

class SurveyDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            survey = get_survey_by_id_string(id_string)
            if survey:
                serializer = SurveyViewSerializer(instance=survey, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    survey_obj = get_survey_by_id_string(id_string)
                    if survey_obj:
                        serializer = SurveySerializer(data=request.data)
                        if serializer.is_valid():
                            survey_obj = serializer.update(survey_obj, serializer.validated_data, request.user)
                            serializer = SurveyViewSerializer(instance=survey_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                DATA: serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
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
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
