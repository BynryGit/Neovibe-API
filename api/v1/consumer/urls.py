from django.urls import path
from v1.consumer.views.consumer import Consumer, ConsumerBills

urlpatterns = [
    path('<uuid:id_string>/', Consumer.as_view()),
    path('bills', ConsumerBills.as_view())
]