__author__ = "aki"

from django.urls import path
from v1.meter_data_management.views.schedule import Schedule, ScheduleList, ScheduleDetail

urlpatterns = [
    path('schedule', Schedule.as_view(), name='schedule'),
    path('schedule/list', ScheduleList.as_view(), name='schedule_list'),
    path('schedule/<uuid:id_string>', ScheduleDetail.as_view(), name='schedule_detail'),
]