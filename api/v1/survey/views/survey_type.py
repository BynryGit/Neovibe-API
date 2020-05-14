from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.survey.models.survey_type import SurveyType,get_survey_type_by_id_string
from v1.survey.serializers.survey_type import SurveyTypeListSerializer,SurveyTypeViewSerializer

# type/list/
class SurveyTypeList(generics.ListAPIView):
    serializer_class = SurveyTypeListSerializer
    pagination_class = StandardResultsSetPagination

    queryset = SurveyType.objects.filter(tenant=1, utility=1)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name', 'tenant__id_string',)
    ordering_fields = ('name', 'tenant',)
    ordering = ('name',)  # always give by default alphabetical order
    search_fields = ('name', 'tenant__name',)

# survey/type/:id_string
class SurveyTypeView(GenericAPIView):
    def get(self,request,id_string):
        try:
            survey_type = get_survey_type_by_id_string(id_string)
            if survey_type:
                serializer = SurveyTypeViewSerializer(instance=survey_type,context={'request':request})
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