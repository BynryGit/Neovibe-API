__author__ = "Priyanka"
import logging
import traceback
from rest_framework.response import Response
from api.messages import SUCCESS,STATE,ERROR,EXCEPTION,DATA
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status

from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.survey.models.survey import get_survey_by_id_string,Survey
from v1.survey.models.survey_status import get_survey_status_by_id_string,get_survey_status_by_id
from v1.survey.models.survey_type import get_survey_type_by_id_string,get_survey_type_by_id
from v1.commonapp.models.area import get_area_by_id,get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id,get_sub_area_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.survey.serializers.survey import SurveyViewSerializer,SurveyListSerializer,SurveySerializer
from v1.commonapp.views.logger import logger



# API Header
# API end Point: api/v1/survey
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Survey
# Interaction: Survey list
# Usage: API will fetch required data for Location and consumer Survey list
# Tables used: 2.3.1 Survey Master,2.3.4 Survey Consumer
# Author: Priyanka
# Created on: 28/04/2020


# API for getting list data of Location Survey
class SurveyList(generics.ListAPIView):
    serializer_class = SurveyListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        try:
            search_str = self.request.query_params.get('search', None)

            queryset = Survey.objects.filter(is_active=True)
            utility_id_string = self.request.query_params.get('utility', None)
            category_id_string = self.request.query_params.get('category', None)
            sub_category_id_string = self.request.query_params.get('sub_category', None)
            area_id_string = self.request.query_params.get('area', None)
            sub_area_id_string = self.request.query_params.get('sub_area', None)
            type_id_string = self.request.query_params.get('type', None)
            objective_id_string = self.request.query_params.get('objective', None)
            status_id_string = self.request.query_params.get('status', None)

            if utility_id_string is not None:
                queryset = queryset.filter(utility__id_string=utility_id_string)
            if category_id_string is not None:
                category = get_consumer_category_by_id_string(category_id_string)
                queryset = queryset.filter(consumer_category_id=category.id)
            if sub_category_id_string is not None:
                sub_category = get_consumer_sub_category_by_id_string(sub_category_id_string)
                queryset = queryset.filter(sub_category_id=sub_category.id)
            if area_id_string is not None:
                area = get_area_by_id_string(area_id_string)
                queryset = queryset.filter(area_id=area.id)
            if sub_area_id_string is not None:
                sub_area = get_sub_area_by_id_string(sub_area_id_string)
                queryset = queryset.filter(sub_area_id=sub_area.id)
            if type_id_string is not  None:
                type = get_survey_type_by_id_string(type_id_string)
                queryset = queryset.filter(type_id=type.id)
            if objective_id_string is not  None:
                objective = get_survey_type_by_id_string(objective_id_string)
                queryset = queryset.filter(objective_id=objective.id)
            if status_id_string is not  None:
                status = get_survey_status_by_id_string(status_id_string)
                queryset = queryset.filter(status_id=status.id)

            if search_str is not None:
                queryset = Survey.objects.filter(is_active=True, name__icontains=search_str).order_by('-id')

            return queryset
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    user = UserDetail.objects.get(id=2)
                    if is_data_verified(request):
                        # Request data verification end
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
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
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

                    survey_obj = get_survey_by_id_string(id_string)
                    if survey_obj:
                        serializer = SurveySerializer(data=id_string)
                        if serializer.is_valid():
                            serializer.update(survey_obj, serializer.validated_data, request.user)
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: serializer.data,
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
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
