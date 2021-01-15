__author__ = "aki"

from django.urls import path
from v1.meter_data_management.views.read_cycle import ReadCycleList
from v1.meter_data_management.views.schedule_log import ScheduleLogList
from v1.meter_data_management.views.schedule import Schedule, ScheduleList, ScheduleDetail


urlpatterns = [
    path('schedule', Schedule.as_view(), name='schedule'),
    path('schedule/list', ScheduleList.as_view(), name='schedule_list'),
    path('schedule/<uuid:id_string>', ScheduleDetail.as_view(), name='schedule_detail'),
    path('schedule-log/list', ScheduleLogList.as_view(), name='schedule_log_list'),
    path('utility/<uuid:id_string>/read_cycle/list', ReadCycleList.as_view(), name='read_cycle_list'),
]