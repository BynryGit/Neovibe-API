__author__ = "aki"

from django.urls import path
from v1.meter_reading.views.bill_cycle import BillCycleList, BillCycleDetail
from v1.meter_reading.views.consumer import consumerList, consumerDetail
from v1.meter_reading.views.job_card import JobcardList
from v1.meter_reading.views.route_assignment import RouteAssignment, RouteAssignmentDetail
from v1.meter_reading.views.meter_reader import MeterReaderList, MeterReaderDetail
from v1.meter_reading.views.meter_reading import MeterReading, MeterReadingList, MeterReadingDetail
from v1.meter_reading.views.route import RouteList, RouteDetail
from v1.meter_reading.views.schedule import Schedule, ScheduleList, ScheduleDetail
from v1.meter_reading.views.validation import ValidationDetail

urlpatterns = [
    path('schedule', Schedule.as_view(), name='schedule'),
    path('schedule/list', ScheduleList.as_view(), name='schedule_list'),
    path('schedule/<uuid:id_string>', ScheduleDetail.as_view(), name='schedule_detail'),

    path('bill-cycle/list', BillCycleList.as_view(), name='billcycle_list'),
    path('bill-cycle/<uuid:id_string>', BillCycleDetail.as_view(), name='billcycle_detail'),

    path('route/list', RouteList.as_view(), name='route_list'),
    path('route/<uuid:id_string>', RouteDetail.as_view(), name='route_detail'),

    path('route/<uuid:id_string>/assign', RouteAssignment.as_view(), name='route_assignment'),
    path('route/<uuid:route>/deassign/<uuid:route_assignment>', RouteAssignmentDetail.as_view(), name='route_assignment_detail'),

    path('job-card/list', JobcardList.as_view(), name='job_card_list'),

    path('consumer/list', consumerList.as_view(), name='consumer_list'),
    path('consumer/<uuid:id_string>', consumerDetail.as_view(), name='consumer_detail'),

    path('meterreader/list', MeterReaderList.as_view(), name='meter_reader_list'),
    path('meterreader/<uuid:id_string>', MeterReaderDetail.as_view(), name='meter_reader_detail'),

    path('meterreading', MeterReading.as_view(), name='MeterReading'),
    path('meterreading/list', MeterReadingList.as_view(), name='meter_reading_list'),
    path('meterreading/<uuid:id_string>', MeterReadingDetail.as_view(), name='meter_reading_detail'),

    path('meterreading/<uuid:id_string>/validate', ValidationDetail.as_view(), name='validation_detail'),
]