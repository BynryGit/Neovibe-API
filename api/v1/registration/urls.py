from django.urls import path
from v1.registration.views.registrations import RegistrationList, Registration

urlpatterns = [
    path('', RegistrationList.as_view()),
    path('<uuid:id_string>/', Registration.as_view()),
]