__author__ = "Priyanka"
import logging
import traceback
from rest_framework.response import Response
from api.messages import SUCCESS,STATE,ERROR,EXCEPTION,DATA
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status

from v1.survey.models.survey import get_survey_by_id_string
from v1.survey.models.survey_consumer import SurveyConsumer,get_survey_consumer_by_id_string
from v1.survey.serializers.consumers import ConsumerListSerializer,ConsumerViewSerializer
from v1.commonapp.views.logger import logger

# API Header
# API end Point: api/v1/survey/:id-string/consumers
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Consumer Survey
# Interaction: View Consumer list
# Usage: View
# Tables used: 2.3.4 Survey Consumer
# Auther: Priyanka
# Created on: 29/04/2020

class ConsumerList(GenericAPIView):

    def get(self,request,id_string):
        try:
            survey_obj = get_survey_by_id_string(id_string)
            if survey_obj:
                consumers_obj = SurveyConsumer.objects.filter(survey_id=survey_obj.id, is_active=True)
                if consumers_obj:
                    serializer = ConsumerListSerializer(consumers_obj,many=True, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        DATA: serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        DATA: '',
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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


# API Header
# API end Point: api/v1/survey/consumer/:id_string
# API verb: GET, POST, PUT
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

