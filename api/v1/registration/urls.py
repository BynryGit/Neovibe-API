from django.urls import path
from v1.registration.views.registration import RegistrationList, Registration, RegistrationDetail

urlpatterns = [
    path('list', RegistrationList.as_view()),
    path('<uuid:id_string>', RegistrationDetail.as_view()),
    path('', Registration.as_view())
]