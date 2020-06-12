__author__ = "aki"

from django.urls import path

from v1.meter_reading.views.bill_cycle import BillCycleList, BillCycleDetail
from v1.meter_reading.views.route import RouteList, RouteDetail
from v1.meter_reading.views.schedule import Schedule, ScheduleList, ScheduleDetail

urlpatterns = [
    path('schedule', Schedule.as_view(), name='schedule'),
    path('schedule/list', ScheduleList.as_view(), name='schedule_list'),
    path('schedule/<uuid:id_string>', ScheduleDetail.as_view(), name='schedule_detail'),

    path('bill-cycle/list', BillCycleList.as_view(), name='billcycle_list'),
    path('bill-cycle/<uuid:id_string>', BillCycleDetail.as_view(), name='billcycle_detail'),

    path('route/list', RouteList.as_view(), name='route_list'),
    path('route/<uuid:id_string>', RouteDetail.as_view(), name='route_detail'),

]