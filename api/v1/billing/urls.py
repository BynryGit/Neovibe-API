from django.urls import path
from  v1.billing.views.bill_cycle import BillCycleList
from v1.billing.views.bill_schedule import ScheduleBill, ScheduleBillList, BillScheduleSummary, ScheduleBillDetail
from v1.billing.task.bill_schedule_log import schedule_bill_log
from v1.billing.views.bill_schedule_log import ScheduleBillLogByBillSchedule

urlpatterns = [
    path('utility/<uuid:id_string>/bill-cycle/list', BillCycleList.as_view(), name="BillCycleList"),
    path('schedule-bill/list',ScheduleBillList.as_view(), name="ScheduleBillList"),
    path('schedule-bill',ScheduleBill.as_view(), name="ScheduleBill"),
    path('schedule-bill/<uuid:id_string>',ScheduleBillDetail.as_view(),name="ScheduleBillDetail"),
    path('utility/<uuid:id_string>/bill-schedule-summary', BillScheduleSummary.as_view(),name='bill_schedule_summary'),
    path('bill-schedule-log', schedule_bill_log, name="schedule_bill_log"),
    path('bill-schedule-log/list', ScheduleBillLogByBillSchedule.as_view(), name="ScheduleBillLogByBillSchedule")
]