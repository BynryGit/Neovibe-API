from django.urls import path
from  v1.billing.views.bill_cycle import BillCycleList
from v1.billing.views.bill_schedule import ScheduleBill, ScheduleBillList

urlpatterns = [
    path('utility/<uuid:id_string>/bill-cycle/list', BillCycleList.as_view(), name="BillCycleList"),
    path('schedule-bill/list',ScheduleBillList.as_view(), name="ScheduleBillList"),
    path('schedule-bill',ScheduleBill.as_view(), name="ScheduleBill")
]