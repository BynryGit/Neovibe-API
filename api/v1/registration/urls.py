from django.urls import path
from v1.registration.views.registrations import RegistrationList, Registration

urlpatterns = [
    path('', Registration.as_view()),
    path('list/', RegistrationList.as_view())
]