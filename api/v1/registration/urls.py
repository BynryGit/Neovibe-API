from django.urls import path
from v1.registration.views.registrations import RegistrationListApiView

urlpatterns = [
    path('list/', RegistrationListApiView.as_view())
]