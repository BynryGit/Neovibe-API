from django.urls import path
from v1.survey.views.survey import SurveyListApiView,Surveys,ConsumerSurveyApiView,ConsumerList

urlpatterns = [
    path('', SurveyListApiView.as_view(),name="survey_list"),
    path('<uuid:id_string>/', Surveys.as_view(),name="survey_data"),
    path('consumer/<uuid:id_string>', ConsumerSurveyApiView.as_view()),
    path('<uuid:id_string>/consumers/', ConsumerList.as_view())
]