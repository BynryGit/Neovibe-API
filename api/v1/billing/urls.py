from django.urls import path
from  v1.billing.views.bill_cycle import BillCycleList

urlpatterns = [
    path('utility/<uuid:id_string>/bill-cycle/list', BillCycleList.as_view(), name="BillCycleList"),
]