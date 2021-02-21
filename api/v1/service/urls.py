from django.urls import path


from v1.service.views.consumer_service_details import ServiceList

urlpatterns = [
    path('utility/<uuid:id_string>/list', ServiceList.as_view()),
]