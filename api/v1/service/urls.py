from django.urls import path

from v1.service.views.consumer_service_master import ConsumerServiceMasterList, ConsumerServiceMaster, ConsumerServiceMasterDetail
from v1.service.views.consumer_service_details import ServiceList

urlpatterns = [
    path('utility/<uuid:id_string>/list', ServiceList.as_view()),
    path('<uuid:id_string>/list', ConsumerServiceMasterList.as_view()),
    path('', ConsumerServiceMaster.as_view()),
    path('<uuid:id_string>', ConsumerServiceMasterDetail.as_view())
]