from django.urls import path
from v1.registration.views.registration import *
from v1.registration.views.registration_type import *
from v1.registration.views.registration_subtype import *

urlpatterns = [
    path('list', RegistrationList.as_view()),
    path('status-list', RegistrationStatusList.as_view()),
    path('<uuid:id_string>', RegistrationDetail.as_view()),
    path('', Registration.as_view()),
    path('<uuid:id_string>/payment', RegistrationPayment.as_view()),
    path('<uuid:id_string>/payment/list', RegistrationPaymentList.as_view()),
    path('payment/<uuid:id_string>/approve', RegistrationPaymentApprove.as_view()),
    path('payment/<uuid:id_string>/reject', RegistrationPaymentReject.as_view()),
    path('<uuid:id_string>/reject', RegistrationReject.as_view()),
    path('<uuid:id_string>/hold', RegistrationHold.as_view()),
    path('<uuid:id_string>/approve', RegistrationApprove.as_view()),
    path('<uuid:id_string>/note/list', RegistrationNoteList.as_view()),
    path('<uuid:id_string>/note', RegistrationNote.as_view()),
    path('life-cycles', RegistrationLifeCycleList.as_view()),
    path('payment/<uuid:id_string>/transaction/list', RegistrationPaymentTransactionList.as_view()),
    path('utility/<uuid:id_string>/type/list', RegistrationTypeList.as_view(),name="registration_type_list"),
    path('type/<uuid:id_string>', RegistrationTypeDetail.as_view(),name="registration_type_detail"),
    path('type', RegistrationType.as_view(),name="registration_type"),
    path('utility/<uuid:id_string>/subtype/list', RegistrationSubTypeList.as_view(),name="registration_subtype_list"),
    path('subtype/<uuid:id_string>', RegistrationSubTypeDetail.as_view(),name="registartion_subtype_detail"),
    path('subtype', RegistrationSubType.as_view(),name="registration_subtype")
]