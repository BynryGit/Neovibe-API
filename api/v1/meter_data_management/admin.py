__author__ = "aki"


from django.contrib import admin
from v1.meter_data_management.models.meter import Meter
from v1.meter_data_management.models.meter_make import MeterMake
from v1.meter_data_management.models.meter_reading import MeterReading
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment
from v1.meter_data_management.models.schedule import Schedule
from v1.meter_data_management.models.schedule_log import ScheduleLog
from v1.meter_data_management.models.read_cycle import ReadCycle
from v1.meter_data_management.models.route import Route
from v1.meter_data_management.models.consumer_detail import ConsumerDetail
from v1.meter_data_management.models.smart_meter_configuration import SmartMeterConfiguration
from v1.meter_data_management.models.job_card_template import JobCardTemplate
from v1.meter_data_management.models.validation_assignments import ValidationAssignment
from v1.meter_data_management.models.reader_status import ReaderStatus

admin.site.register(Meter)
admin.site.register(MeterMake)
admin.site.register(Schedule)
admin.site.register(ScheduleLog)
admin.site.register(ReadCycle)
admin.site.register(Route)
admin.site.register(ConsumerDetail)
admin.site.register(MeterReading)
admin.site.register(RouteTaskAssignment)
admin.site.register(SmartMeterConfiguration)
admin.site.register(JobCardTemplate)
admin.site.register(ValidationAssignment)
admin.site.register(ReaderStatus)
