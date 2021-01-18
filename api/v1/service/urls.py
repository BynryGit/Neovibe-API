from django.urls import path

from v1.service.views.consumer_service_master import ConsumerServiceMasterList
from v1.service.views.service import ServiceList

urlpatterns = [
    path('utility/<uuid:id_string>/list', ServiceList.as_view()),
    path('<uuid:id_string>/list', ConsumerServiceMasterList.as_view())
]