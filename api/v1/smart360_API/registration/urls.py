from django.urls import path

from api.v1.smart360_API.registration.views.registrations import RegistrationListApiView, RegistrationApiView

urlpatterns = [
    path('', RegistrationApiView.as_view()),
    path('list', RegistrationListApiView.as_view()),
]