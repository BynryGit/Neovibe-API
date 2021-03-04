__author__ = "aki"

from django.urls import path
from v1.meter_data_management.task.schedule_log import schedule_log
from v1.meter_data_management.views.meter_make import MeterMakeList
from v1.meter_data_management.views.meter_summary import MeterSummary
from v1.meter_data_management.views.read_cycle import ReadCycleList
from v1.meter_data_management.views.read_cycle import ReadCycle,ReadCycleShortList,ReadCycleDetail
from v1.meter_data_management.views.route import RouteList, RouteDetail, Route, RouteShortList
from v1.meter_data_management.views.schedule_log import ScheduleLogList, ReadingScheduleLogSummary, ScheduleLogDetail
from v1.meter_data_management.views.schedule_log_route import ScheduleLogRouteList
from v1.meter_data_management.views.smart_meter_configuration import SmartMeterList, SmartMeter, SmartMeterDetail
from v1.meter_data_management.views.job_card_template import JobCardTemplateList,JobCardTemplateDetail,JobCardTemplate
from v1.meter_data_management.views.schedule import Schedule, ScheduleList, ScheduleDetail, ReadingScheduleSummary
from v1.meter_data_management.views.validation_assignments import ValidationAssignmentList,ValidationAssignmentDetail,\
    ValidationAssignment
from v1.meter_data_management.views.meter import MeterList, Meter, MeterDetail, MeterLifeCycleList, MeterNoteList, \
    MeterNoteDetail
from v1.meter_data_management.views.route_task_assignment import RouteTaskAssignment, RouteTaskAssignmentList, \
    RouteTaskAssignmentDetail

urlpatterns = [
    path('schedule', Schedule.as_view(), name='schedule'),
    path('schedule/list', ScheduleList.as_view(), name='schedule_list'),
    path('schedule/<uuid:id_string>', ScheduleDetail.as_view(), name='schedule_detail'),
    path('utility/<uuid:id_string>/reading-schedule-summary', ReadingScheduleSummary.as_view(),
         name='reading_schedule_summary'),

    path('schedule-log/list', ScheduleLogList.as_view(), name='schedule_log_list'),
    path('schedule-log/<uuid:id_string>', ScheduleLogDetail.as_view(), name='schedule_detail'),
    path('utility/<uuid:id_string>/reading-schedule-log-summary', ReadingScheduleLogSummary.as_view(),
         name='reading_schedule_summary'),

    path('utility/<uuid:id_string>/read_cycle/list', ReadCycleList.as_view(), name='read_cycle_list'),
    path('utility/<uuid:id_string>/read_cycle/short_list', ReadCycleShortList.as_view(), name='read_cycle_short_list'),
    path('read_cycle/<uuid:id_string>', ReadCycleDetail.as_view(), name='read_cycle_detail'),
    path('read_cycle', ReadCycle.as_view(), name='read_cycle_add'),

    path('utility/<uuid:id_string>/route/list', RouteList.as_view(), name='route_list'),
    path('utility/<uuid:id_string>/route/short_list', RouteShortList.as_view(), name='route_short_list'),
    path('route/<uuid:id_string>', RouteDetail.as_view(), name='route_detail'),
    path('route', Route.as_view(), name='route_add'),
    path('schedule-log/<uuid:id_string>/route/list', ScheduleLogRouteList.as_view(), name='schedule_route_list'),

    path('smart-meter', SmartMeter.as_view()),
    path('<uuid:id_string>/smart-meter/list', SmartMeterList.as_view(), name='meter_list'),
    path('smart-meter/<uuid:id_string>', SmartMeterDetail.as_view(), name='meter_detail'),

    path('task-template', JobCardTemplate.as_view()),
    path('<uuid:id_string>/task-template/list', JobCardTemplateList.as_view()),
    path('task-template/<uuid:id_string>', JobCardTemplateDetail.as_view()),

    path('meter', Meter.as_view(), name='meter'),
    path('meter/list', MeterList.as_view(), name='meter_list'),

    path('validation-assignment/<uuid:id_string>', ValidationAssignmentDetail.as_view()),
    path('validation-assignment', ValidationAssignment.as_view()),
    path('<uuid:id_string>/validation-assignment/list', ValidationAssignmentList.as_view()),

    path('meter/<uuid:id_string>', MeterDetail.as_view()),
    path('meter/note/list',MeterNoteList.as_view(),name="note_list"),
    path('meter/<uuid:id_string>/note', MeterNoteDetail.as_view(), name='meter_note_detail'),
    path('utility/<uuid:id_string>/meter-summary', MeterSummary.as_view(), name='meter_summary'),
    path('meter-make/list', MeterMakeList.as_view(), name="meter_make_list"),
    path('meter/life-cycle/list', MeterLifeCycleList.as_view(), name="life_cycle_list"),

    path('route-task-assignment', RouteTaskAssignment.as_view(), name='route_task_assignment'),
    path('route-task-assignment/list', RouteTaskAssignmentList.as_view(), name='route_task_assignment_list'),
    path('route-task-assignment/<uuid:id_string>', RouteTaskAssignmentDetail.as_view(), name='route_task_assignment_detail'),

    path('log', schedule_log, name='route_add')
]