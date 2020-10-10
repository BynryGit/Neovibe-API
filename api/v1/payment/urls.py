from django.urls import path
from v1.payment.views.payment import *

urlpatterns = [
    path('<uuid:id_string>/approve', PaymentApprove.as_view()),
    path('<uuid:id_string>/reject', PaymentReject.as_view()),
]