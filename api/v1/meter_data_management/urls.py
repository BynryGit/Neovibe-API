__author__ = "aki"

from django.urls import path
from v1.meter_data_management.views.meter_make import MeterMakeList
from v1.meter_data_management.views.meter_reading import MeterReading, MeterReadingList
from v1.meter_data_management.views.new_consumer_detail import NewConsumerDetail, NewConsumerDetailList, \
    NewConsumerDetailView
from v1.meter_data_management.views.schedule_log_read_cycle import ScheduleLogReadCycleList
from v1.meter_data_management.views.validation_summary import ValidationSummary
from v1.meter_data_management.views.meter_reading_validation_one import MeterReadingValidationOneDetail
from v1.meter_data_management.views.meter_reading_validation_two import MeterReadingValidationTwoDetail
from v1.meter_data_management.views.meter_summary import MeterSummary
from v1.meter_data_management.views.read_cycle import ReadCycleList
from v1.meter_data_management.views.schedule_log_route import ScheduleLogRouteList
from v1.meter_data_management.views.route import RouteList, RouteDetail, Route, RouteShortList
from v1.meter_data_management.views.assign_revisit_task_assignment import AssignRevisitTaskAssignment
from v1.meter_data_management.views.read_cycle import ReadCycle,ReadCycleShortList,ReadCycleDetail
from v1.meter_data_management.views.deassign_revisit_task_assignment import DeAssignRevisitTaskAssignment
from v1.meter_data_management.views.smart_meter_configuration import SmartMeterList, SmartMeter, SmartMeterDetail
from v1.meter_data_management.views.schedule import Schedule, ScheduleList, ScheduleDetail, ScheduleSummary
from v1.meter_data_management.views.schedule_log_read_cycle_revisit_task import ScheduleLogReadCycleRevisitTaskList
from v1.meter_data_management.views.schedule_log import ScheduleLogList, ScheduleLogSummary, ScheduleLogDetail
from v1.meter_data_management.views.job_card_template import JobCardTemplateList,JobCardTemplateDetail,JobCardTemplate
from v1.meter_data_management.views.upload_route import UploadRouteList, UploadRoute
from v1.meter_data_management.views.upload_sammary import UploadSummary
from v1.meter_data_management.views.validation import ValidationList
from v1.meter_data_management.views.meter_reading_validation_revisit import MeterReadingValidationRevisitDetail
from v1.meter_data_management.views.validation_schedule_log import ValidationScheduleLogList
from v1.meter_data_management.views.validation_assignments import ValidationAssignmentList,ValidationAssignmentDetail,\
    ValidationAssignment
from v1.meter_data_management.views.meter import MeterList, Meter, MeterDetail, MeterLifeCycleList, MeterNoteList, \
    MeterNoteDetail
from v1.meter_data_management.views.reader_status import ReaderStatusDetail, ReaderStatus, ReaderStatusList
from v1.meter_data_management.views.route_task_assignment import RouteTaskAssignment, RouteTaskAssignmentList, \
    RouteTaskAssignmentDetail

urlpatterns = [

    path('utility/<uuid:id_string>/read_cycle/list', ReadCycleList.as_view(), name='read_cycle_list'),
    path('utility/<uuid:id_string>/read_cycle/short_list', ReadCycleShortList.as_view(), name='read_cycle_short_list'),
    path('read_cycle/<uuid:id_string>', ReadCycleDetail.as_view(), name='read_cycle_detail'),
    path('<uuid:id_string>/read_cycle', ReadCycle.as_view(), name='read_cycle_add'),

    path('utility/<uuid:id_string>/reader-status/list', ReaderStatusList.as_view(), name='read_cycle_list'),
    path('reader-status/<uuid:id_string>', ReaderStatusDetail.as_view(), name='read_cycle_detail'),
    path('reader-status', ReaderStatus.as_view(), name='read_cycle_add'),

    path('utility/<uuid:id_string>/route/list', RouteList.as_view(), name='route_list'),
    path('utility/<uuid:id_string>/route/short_list', RouteShortList.as_view(), name='route_short_list'),
    path('route/<uuid:id_string>', RouteDetail.as_view(), name='route_detail'),
    path('<uuid:id_string>/route', Route.as_view(), name='route_add'),

    path('smart-meter', SmartMeter.as_view()),
    path('<uuid:id_string>/smart-meter/list', SmartMeterList.as_view(), name='meter_list'),
    path('smart-meter/<uuid:id_string>', SmartMeterDetail.as_view(), name='meter_detail'),

    path('task-template', JobCardTemplate.as_view()),
    path('<uuid:id_string>/task-template/list', JobCardTemplateList.as_view()),
    path('task-template/<uuid:id_string>', JobCardTemplateDetail.as_view()),

    path('validation-assignment/<uuid:id_string>', ValidationAssignmentDetail.as_view()),
    path('validation-assignment', ValidationAssignment.as_view()),
    path('<uuid:id_string>/validation-assignment/list', ValidationAssignmentList.as_view()),

    # Schedule API Start
    path('schedule', Schedule.as_view(), name='schedule'),
    path('schedule/list', ScheduleList.as_view(), name='schedule_list'),
    path('schedule/<uuid:id_string>', ScheduleDetail.as_view(), name='schedule_detail'),
    path('schedule/summary', ScheduleSummary.as_view(), name='schedule_summary'),
    # Schedule API End

    # Dispatch API Start
    path('schedule-log/list', ScheduleLogList.as_view(), name='schedule_log_list'),
    path('schedule-log/<uuid:id_string>', ScheduleLogDetail.as_view(), name='schedule_detail'),
    path('schedule-log/summary', ScheduleLogSummary.as_view(), name='schedule_log_summary'),
    path('schedule-log/<uuid:id_string>/route/list', ScheduleLogRouteList.as_view(), name='schedule_log_route_list'),
    path('schedule-log/<uuid:id_string>/read-cycle-revisit-task/list', ScheduleLogReadCycleRevisitTaskList.as_view(),
         name='schedule_log_read_cycle_revisit_task_list'),

    path('route-task-assignment', RouteTaskAssignment.as_view(), name='route_task_assignment'),
    path('route-task-assignment/<uuid:id_string>', RouteTaskAssignmentDetail.as_view(),
         name='route_task_assignment_detail'),
    path('assign-revisit-task-assignment', AssignRevisitTaskAssignment.as_view(),
         name='assign_revisit_task_assignment'),
    path('de-assign-revisit-task-assignment', DeAssignRevisitTaskAssignment.as_view(),
         name='de_revisit_route_task_assignment'),
    # Dispatch API End

    # validation API Start
    path('validation/summary', ValidationSummary.as_view(), name='meter_reading_summary'),
    path('validation-schedule-log/list', ValidationScheduleLogList.as_view(), name='validation_schedule_log_list'),
    path('schedule-log/<uuid:schedule_log>/read-cycle/<uuid:read_cycle>/validation/list',
         ValidationList.as_view(), name='validation_list'),
    path('meter-reading/<uuid:id_string>/validation-one', MeterReadingValidationOneDetail.as_view(),
         name='meter_reading_validation_one_detail'),
    path('meter-reading/<uuid:id_string>/validation-two', MeterReadingValidationTwoDetail.as_view(),
         name='meter_reading_validation_two_detail'),
    path('meter-reading/<uuid:id_string>/validation-revisit', MeterReadingValidationRevisitDetail.as_view(),
         name='validation_revisit_detail'),
    # validation API End

    # Search Consumer API Start
    path('schedule-log/<uuid:id_string>/read-cycle/list', ScheduleLogReadCycleList.as_view(),
         name='schedule_log_read_cycle_list'),
    # Search Consumer API End

    # Upload API Start
    path('upload/summary', UploadSummary.as_view(), name='upload_summary'),
    path('upload-route/list', UploadRouteList.as_view(), name='upload_route_list'),
    path('upload-route', UploadRoute.as_view(), name='upload_route'),
    # Upload API End

    # Meter Master API Start
    path('meter/list', MeterList.as_view(), name='meter_list'),
    path('meter', Meter.as_view(), name='meter'),
    path('meter/<uuid:id_string>', MeterDetail.as_view()),
    path('meter/summary', MeterSummary.as_view(), name='meter_summary'),
    path('meter/note/list', MeterNoteList.as_view(), name="note_list"),
    path('meter/<uuid:id_string>/note', MeterNoteDetail.as_view(), name='meter_note_detail'),
    path('meter-make/list', MeterMakeList.as_view(), name="meter_make_list"),
    path('meter/life-cycle/list', MeterLifeCycleList.as_view(), name="life_cycle_list"),
    path('meter-reading/list', MeterReadingList.as_view(), name="meter_reading_list"),
    # Meter Master API End

    # Mobile Side API Start
    path('route-task-assignment/list', RouteTaskAssignmentList.as_view(),
         name='route_task_assignment_list'),
    path('meter-reading', MeterReading.as_view(), name='meter_reading'),
    path('new-consumer', NewConsumerDetail.as_view(), name='new_consumer'),
    # Mobile Side API End

    # New Consumer API Start
    path('new-consumer/list', NewConsumerDetailList.as_view(), name='new_consumer_detail_list'),
    path('new-consumer/<uuid:id_string>', NewConsumerDetailView.as_view(), name='new_consumer_detail_view'),
    # New Consumer API End
]
