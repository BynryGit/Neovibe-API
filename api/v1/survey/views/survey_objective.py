from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION

from v1.survey.models.survey_objective import SurveyObjective,get_survey_objective_by_id_string
from v1.survey.serializers.survey_objective import SurveyObjectiveListSerializer,SurveyObjectiveViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class SurveyObjectiveList(generics.ListAPIView):
    serializer_class = SurveyObjectiveListSerializer
    pagination_class = StandardResultsSetPagination

    queryset = SurveyObjective.objects.filter(tenant=1, utility=1)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('objective', 'tenant__id_string',)
    ordering_fields = ('objective', 'tenant',)
    ordering = ('objective',)  # always give by default alphabetical order
    search_fields = ('objective', 'tenant__name',)



class SurveyObjectiveView(GenericAPIView):
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
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
