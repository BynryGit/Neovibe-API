from django.urls import path
from v1.billing.views.billing import InvoiceBill, InvoiceBillDetail

urlpatterns = [
    path('', InvoiceBill.as_view()),
    path('<uuid:id_string>', InvoiceBillDetail.as_view()),
]