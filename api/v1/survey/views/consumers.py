__author__ = "Priyanka"
import logging
import traceback
from rest_framework.response import Response
from api.messages import SUCCESS,STATE,ERROR,EXCEPTION,DATA,RESULTS
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.userapp.models.user_master import UserDetail
from v1.survey.models.survey import get_survey_by_id_string
from v1.survey.models.survey_consumer import SurveyConsumer,get_survey_consumer_by_id_string
from v1.survey.serializers.consumers import ConsumerSerializer
from v1.survey.serializers.consumers import ConsumerViewSerializer,ConsumerSerializer
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.survey.views.common_functions import is_data_verified

# API Header
# API end Point: api/v1/survey/:id-string/consumer-list
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Consumer Survey
# Interaction: View Consumer list
# Usage: View
# Tables used: 2.3.4 Survey Consumer
# Auther: Priyanka
# Created on: 29/04/2020

class ConsumerList(generics.ListAPIView):
    try:
        serializer_class = ConsumerViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('first_name', 'consumer_no',)
        ordering_fields = ('first_name',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('first_name',)

        def get_queryset(self):
            if is_token_valid(1):
                if is_authorized():
                    queryset = ''
                    survey = get_survey_by_id_string(self.kwargs['id_string'])
                    if survey:
                        queryset = SurveyConsumer.objects.filter(survey_id=survey.id, is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/survey/:id_string/consumers
# API verb: POST
# Package: Basic
# Modules: S&M
# Sub Module: Consumer Survey
# Interaction:  Add Consumer Survey
# Usage: Add Consumer Survey
# Tables used: 2.3.4 Survey Consumer
# Auther: Priyanka
# Created on: 19/05/2020

class Consumers(GenericAPIView):
    def post(self, request,id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    user = UserDetail.objects.get(id=2)
                    if is_data_verified(request):
                        survey = get_survey_by_id_string(id_string)
                        if survey:
                            serializer = ConsumerSerializer(data=request.data)
                            if serializer.is_valid():
                                survey_obj = serializer.create(serializer.validated_data, user,survey)
                                view_serializer = ConsumerViewSerializer(instance=survey_obj,
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
                            }, status=status.HTTP_204_NO_CONTENT)
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
# API end Point: api/v1/survey/consumer/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: S&M
# Sub Module: Consumer Survey
# Interaction: View Consumer Survey, Add Consumer Survey, Edit Consumer Survey
# Usage: View, Add, Edit Consumer Survey
# Tables used: 2.3.1 Survey Master,2.3.4 Survey Consumer
# Auther: Priyanka
# Created on: 29/04/2020

class ConsumerDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            consumer_survey = get_survey_consumer_by_id_string(id_string)
            if consumer_survey:
                serializer = ConsumerViewSerializer(instance=consumer_survey, context={'request': request})
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    user = UserDetail.objects.get(id=2)
                    print()
                    consumer_obj = get_survey_consumer_by_id_string(id_string)
                    if consumer_obj:
                        serializer = ConsumerSerializer(data=request.data)
                        if serializer.is_valid():
                            consumer_obj = serializer.update(consumer_obj, serializer.validated_data, user)
                            view_serializer = ConsumerViewSerializer(instance=consumer_obj,context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
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


