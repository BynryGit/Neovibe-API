from django.urls import path
from v1.service.views.service import ServiceList

urlpatterns = [
    path('utility/<uuid:id_string>/list', ServiceList.as_view(),name="survey_list"),
    

    
]