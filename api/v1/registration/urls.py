from django.urls import path
from v1.registration.views.registration import *

urlpatterns = [
    path('list', RegistrationList.as_view()),
    path('status-list', RegistrationStatusList.as_view()),
    path('<uuid:id_string>', RegistrationDetail.as_view()),
    path('', Registration.as_view()),
    path('<uuid:id_string>/payment', RegistrationPayment.as_view()),
    path('<uuid:id_string>/payment', RegistrationPaymentDetail.as_view()),
    path('payment/<uuid:id_string>/approve', RegistrationPaymentApprove.as_view()),
    path('payment/<uuid:id_string>/reject', RegistrationPaymentReject.as_view()),
    path('<uuid:id_string>/reject', RegistrationReject.as_view()),
    path('<uuid:id_string>/hold', RegistrationHold.as_view()),
]