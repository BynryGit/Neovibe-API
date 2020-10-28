from django.urls import path
from v1.registration.views.registration import *

urlpatterns = [
    path('list', RegistrationList.as_view()),
    path('status-list', RegistrationStatusList.as_view()),
    path('<uuid:id_string>', RegistrationDetail.as_view()),
    path('', Registration.as_view()),
    path('<uuid:id_string>/payment', RegistrationPayment.as_view()),
    path('<uuid:id_string>/payments', RegistrationPaymentList.as_view()),
    path('payment/<uuid:id_string>/approve', RegistrationPaymentApprove.as_view()),
    path('payment/<uuid:id_string>/reject', RegistrationPaymentReject.as_view()),
    path('<uuid:id_string>/reject', RegistrationReject.as_view()),
    path('<uuid:id_string>/hold', RegistrationHold.as_view()),
    path('<uuid:id_string>/approve', RegistrationApprove.as_view()),
    path('<uuid:id_string>/notes', RegistrationNoteList.as_view()),
    path('<uuid:id_string>/note', RegistrationNote.as_view()),
    path('<uuid:id_string>/life-cycles', RegistrationLifeCycleList.as_view()),
    path('payment/<uuid:id_string>/transactions', RegistrationPaymentTransactionList.as_view()),
]