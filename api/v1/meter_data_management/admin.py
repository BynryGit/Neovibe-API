__author__ = "aki"


from django.contrib import admin
from v1.meter_data_management.models.meter import Meter
from v1.meter_data_management.models.schedule import Schedule
from v1.meter_data_management.models.schedule_log import ScheduleLog
from v1.meter_data_management.models.read_cycle import ReadCycle
from v1.meter_data_management.models.route import Route
from v1.meter_data_management.models.consumer_detail import ConsumerDetail


admin.site.register(Meter)
admin.site.register(Schedule)
admin.site.register(ScheduleLog)
admin.site.register(ReadCycle)
admin.site.register(Route)
admin.site.register(ConsumerDetail)
