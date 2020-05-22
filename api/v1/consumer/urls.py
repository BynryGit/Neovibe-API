from django.urls import path
from v1.consumer.views.consumer import *

urlpatterns = [
    path('<uuid:id_string>', ConsumerDetail.as_view()),
    path('', Consumer.as_view()),
    path('<uuid:id_string>/bill/list', ConsumerBillList.as_view()),
    path('bill/<uuid:id_string>', ConsumerBillDetail.as_view()),
    path('<uuid:id_string>/payment',ConsumerPayment.as_view()),
    path('payment/<uuid:id_string>',ConsumerPaymentDetail.as_view()),
    path('<uuid:id_string>/payment/list',ConsumerPaymentList.as_view()),
    path('<uuid:id_string>/complaint/list',ConsumerComplaintList.as_view()),
]