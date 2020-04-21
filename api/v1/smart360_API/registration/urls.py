from django.urls import path

from api.v1.smart360_API.registration.views.registrations import RegistrationListApiView

urlpatterns = [
    path('list', RegistrationListApiView.as_view()),
]