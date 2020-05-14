from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.survey.models.survey_status import SurveyStatus,get_survey_status_by_id_string
from v1.survey.serializers.survey_status import SurveyStatusListSerializer,SurveyStatusViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

# status/list/
class SurveyStatusList(generics.ListAPIView):
    serializer_class = SurveyStatusListSerializer
    pagination_class = StandardResultsSetPagination

    queryset = SurveyStatus.objects.filter(tenant=1, utility=1)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name', 'tenant__id_string',)
    ordering_fields = ('name', 'tenant',)
    ordering = ('name',)  # always give by default alphabetical order
    search_fields = ('name', 'tenant__name',)


# status/<uuid:id_string>/
class SurveyStatusView(GenericAPIView):
    def get(self,request,id_string):
        try:
            survey_status = get_survey_status_by_id_string(id_string)
            if survey_status:
                serializer = SurveyStatusViewSerializer(instance=survey_status,context={'request':request})
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
