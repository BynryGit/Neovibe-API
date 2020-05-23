from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.survey.models.survey_objective import SurveyObjective,get_survey_objective_by_id_string
from v1.survey.serializers.survey_objective import SurveyObjectiveListSerializer,SurveyObjectiveViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized


class SurveyObjectiveList(generics.ListAPIView):
    try:
        serializer_class = SurveyObjectiveListSerializer
        pagination_class = StandardResultsSetPagination


        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('objective', 'tenant__id_string',)
        ordering_fields = ('objective', 'tenant',)
        ordering = ('objective',)  # always give by default alphabetical order
        search_fields = ('objective', 'tenant__name',)

        def get_queryset(self):
            if is_token_valid(0):
                if is_authorized():
                    queryset = SurveyObjective.objects.filter(tenant=1, utility=1)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException



class SurveyObjectiveDetail(GenericAPIView):
    def get(self,request,id_string):
        try:
            survey_objective = get_survey_objective_by_id_string(id_string)
            if survey_objective:
                serializer = SurveyObjectiveViewSerializer(instance=survey_objective,context={'request':request})
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
