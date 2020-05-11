from django.urls import path
from v1.registration.views.registrations import RegistrationList, Registration

urlpatterns = [
    path('list', RegistrationList.as_view()),
    path('', Registration.as_view()),
]