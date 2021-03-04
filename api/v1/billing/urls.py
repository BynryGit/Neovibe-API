from django.urls import path
from  v1.billing.views.bill_cycle import BillCycleList
from v1.billing.views.bill_schedule import ScheduleBill, ScheduleBillList, BillScheduleSummary, ScheduleBillDetail

urlpatterns = [
    path('utility/<uuid:id_string>/bill-cycle/list', BillCycleList.as_view(), name="BillCycleList"),
    path('schedule-bill/list',ScheduleBillList.as_view(), name="ScheduleBillList"),
    path('schedule-bill',ScheduleBill.as_view(), name="ScheduleBill"),
    path('schedule-bill/<uuid:id_string>',ScheduleBillDetail.as_view(),name="ScheduleBillDetail"),
    path('utility/<uuid:id_string>/bill-schedule-summary', BillScheduleSummary.as_view(),name='bill_schedule_summary'),
]