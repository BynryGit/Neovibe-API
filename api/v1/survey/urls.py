from django.urls import path
from v1.survey.views.survey import SurveyListApiView,LocationSurveyApiView,ConsumerSurveyApiView

urlpatterns = [
    path('', SurveyListApiView.as_view(),name="survey_list"),
    path('<uuid:id_string>/', LocationSurveyApiView.as_view(),name="survey_data"),
    path('consumer/<uuid:id_string>', ConsumerSurveyApiView.as_view())
]