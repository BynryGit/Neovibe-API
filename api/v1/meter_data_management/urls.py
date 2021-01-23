__author__ = "aki"

from django.urls import path
from v1.meter_data_management.views.schedule import Schedule, ScheduleList, ScheduleDetail
from v1.meter_data_management.views.read_cycle import ReadCycleList,ReadCycle,ReadCycleShortList,ReadCycleDetail
from v1.meter_data_management.views.route import RouteList, RouteDetail, Route, RouteShortList
from v1.meter_data_management.views.read_cycle import ReadCycleList
from v1.meter_data_management.views.schedule_log import ScheduleLogList
from v1.meter_data_management.views.schedule import Schedule, ScheduleList, ScheduleDetail


urlpatterns = [
    path('schedule', Schedule.as_view(), name='schedule'),
    path('schedule/list', ScheduleList.as_view(), name='schedule_list'),
    path('schedule/<uuid:id_string>', ScheduleDetail.as_view(), name='schedule_detail'),
    path('schedule-log/list', ScheduleLogList.as_view(), name='schedule_log_list'),
    path('utility/<uuid:id_string>/read_cycle/list', ReadCycleList.as_view(), name='read_cycle_list'),
    path('utility/<uuid:id_string>/read_cycle/short_list', ReadCycleShortList.as_view(), name='read_cycle_short_list'),
    path('read_cycle/<uuid:id_string>', ReadCycleDetail.as_view(), name='read_cycle_detail'),
    path('read_cycle', ReadCycle.as_view(), name='read_cycle_add'),
    path('utility/<uuid:id_string>/route/list', RouteList.as_view(), name='route_list'),
    path('utility/<uuid:id_string>/route/short_list', RouteShortList.as_view(), name='route_short_list'),
    path('route/<uuid:id_string>', RouteDetail.as_view(), name='route_detail'),
    path('route', Route.as_view(), name='route_add')
]