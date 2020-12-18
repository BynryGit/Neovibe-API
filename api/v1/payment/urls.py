from django.urls import path
from v1.payment.views.payment import *
from v1.payment.views.payment_channel import PaymentChannelList
from v1.payment.views.payment_mode import PaymentModeList
from v1.payment.views.payment_sub_type import PaymentSubTypeList, PaymentSubType, PaymentSubTypeDetail
from v1.payment.views.payment_type import PaymentTypeList, PaymentTypeDetail, PaymentType
from v1.payment.views.payment_mode import PaymentModeList, PaymentModeDetail, PaymentMode

urlpatterns = [
    path('<uuid:id_string>/approve', PaymentApprove.as_view()),
    path('<uuid:id_string>/reject', PaymentReject.as_view()),
    path('type/list', PaymentTypeList.as_view()),
    path('type/<uuid:id_string>', PaymentTypeDetail.as_view()),
    path('type', PaymentType.as_view()),
    path('subtype/list', PaymentSubTypeList.as_view()),
    path('subtype/<uuid:id_string>', PaymentSubTypeDetail.as_view()),
    path('subtype', PaymentSubType.as_view()),
    path('mode/list', PaymentModeList.as_view()),
    path('mode/<uuid:id_string>', PaymentModeDetail.as_view()),
    path('mode', PaymentMode.as_view()),
    path('payment-sub-types', PaymentSubTypeList.as_view()),
    path('<uuid:id_string>/payment-modes', PaymentModeList.as_view()),
    path('<uuid:id_string>/payment-channels', PaymentChannelList.as_view()),

]
