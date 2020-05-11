from django.urls import path
from v1.survey.views.survey import SurveyListApiView,LocationSurveyApiView,ConsumerSurveyApiView

urlpatterns = [
    path('', LocationSurveyApiView.as_view()),
    path('list/', SurveyListApiView.as_view(),name="survey_list"),
    path('consumer/', ConsumerSurveyApiView.as_view())
]