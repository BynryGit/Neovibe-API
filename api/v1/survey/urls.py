from django.urls import path
from v1.survey.views.survey import SurveyListApiView,Surveys
from v1.survey.views.consumers import ConsumerView,ConsumerList
from v1.survey.views.survey_type import SurveyTypeList,SurveyTypeView
from v1.survey.views.survey_status import SurveyStatusList,SurveyStatusView
from v1.survey.views.survey_objective import SurveyObjectiveList,SurveyObjectiveView

urlpatterns = [
    path('', SurveyListApiView.as_view(),name="survey_list"),
    path('<uuid:id_string>/', Surveys.as_view(),name="survey_data"),
    path('consumer/<uuid:id_string>', ConsumerView.as_view(),name="survey_consumer"),
    path('<uuid:id_string>/consumers', ConsumerList.as_view(),name="survey_consumer_list"),
    path('type/list/', SurveyTypeList.as_view(),name="survey_type_list"),
    path('type/<uuid:id_string>/', SurveyTypeView.as_view(),name="survey_type"),
    path('status/list/', SurveyStatusList.as_view(),name="survey_status_list"),
    path('status/<uuid:id_string>/', SurveyStatusView.as_view(),name="survey_status"),
    path('objective/list/', SurveyObjectiveList.as_view(),name="survey_objective_list"),
    path('objective/<uuid:id_string>/', SurveyObjectiveView.as_view(),name="survey_objective"),
]