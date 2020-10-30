from django.urls import path
from v1.payment.views.payment import *
from v1.payment.views.payment_channel import PaymentChannelList
from v1.payment.views.payment_mode import PaymentModeList
from v1.payment.views.payment_sub_type import PaymentSubTypeList
from v1.payment.views.payment_type import PaymentTypeList

urlpatterns = [
    path('<uuid:id_string>/approve', PaymentApprove.as_view()),
    path('<uuid:id_string>/reject', PaymentReject.as_view()),
    path('payment-types', PaymentTypeList.as_view()),
    path('payment-sub-types', PaymentSubTypeList.as_view()),
    path('<uuid:id_string>/payment-modes', PaymentModeList.as_view()),
    path('<uuid:id_string>/payment-channels', PaymentChannelList.as_view()),
]