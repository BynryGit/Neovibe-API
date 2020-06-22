__author__ = "aki"


from django.contrib import admin
from v1.meter_reading.models.activity_type import ActivityType
from v1.meter_reading.models.bill_cycle import BillCycle
from v1.meter_reading.models.bill_cycle_reading_allocation import BillCycleReadingAllocation
from v1.meter_reading.models.consumer import Consumer
from v1.meter_reading.models.jobcard import Jobcard
from v1.meter_reading.models.jobcard_status import JobCardStatus
from v1.meter_reading.models.meter_image_type import MeterImageType
from v1.meter_reading.models.meter_status import MeterStatus
from v1.meter_reading.models.reader_status import ReaderStatus
from v1.meter_reading.models.reading_additional_parameters import ReadingAdditionalParameters
from v1.meter_reading.models.reading_status import ReadingStatus
from v1.meter_reading.models.reading_taken_by import ReadingTakenBy
from v1.meter_reading.models.route import Route
from v1.meter_reading.models.route_assignment import RouteAssignment
from v1.meter_reading.models.route_assignment_status import RouteAssignmentStatus
from v1.meter_reading.models.route_upload import RouteUpload
from v1.meter_reading.models.route_upload_status import RouteUploadStatus
from v1.meter_reading.models.schedule import Schedule
from v1.meter_reading.models.schedule_status import ScheduleStatus
from v1.meter_reading.models.schedule_type import ScheduleType
from v1.meter_reading.models.smart_meter_data import SmartMeterData
from v1.meter_reading.models.unit import Unit
from v1.meter_reading.models.validation import Validation
from v1.meter_reading.models.validation_type import ValidationType


admin.site.register(ActivityType)
admin.site.register(BillCycle)
admin.site.register(BillCycleReadingAllocation)
admin.site.register(Consumer)
admin.site.register(Jobcard)
admin.site.register(JobCardStatus)
admin.site.register(MeterImageType)
admin.site.register(MeterStatus)
admin.site.register(ReaderStatus)
admin.site.register(ReadingAdditionalParameters)
admin.site.register(ReadingStatus)
admin.site.register(ReadingTakenBy)
admin.site.register(Route)
admin.site.register(RouteAssignment)
admin.site.register(RouteAssignmentStatus)
admin.site.register(RouteUpload)
admin.site.register(RouteUploadStatus)
admin.site.register(Schedule)
admin.site.register(ScheduleStatus)
admin.site.register(ScheduleType)
admin.site.register(SmartMeterData)
admin.site.register(Unit)
admin.site.register(Validation)
admin.site.register(ValidationType)
