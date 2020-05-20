from django.urls import path
from v1.consumer.views.consumer import Consumer, ConsumerDetail, ConsumerBillList, ConsumerBillDetail

urlpatterns = [
    path('<uuid:id_string>', ConsumerDetail.as_view()),
    path('', Consumer.as_view()),
    path('<uuid:id_string>/bill/list', ConsumerBillList.as_view()),
    path('bill/<uuid:id_string>', ConsumerBillDetail.as_view()),
]