from django.urls import path
from v1.survey.views.survey import SurveyListApiView,LocationSurveyApiView

urlpatterns = [
    path('', LocationSurveyApiView.as_view()),
    path('list/', SurveyListApiView.as_view())
]