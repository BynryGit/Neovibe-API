__author__ = "aki"


from django.contrib import admin
from v1.meter_data_management.models.meter import Meter
from v1.meter_data_management.models.schedule import Schedule
from v1.meter_data_management.models.schedule_log import ScheduleLog

admin.site.register(Meter)
admin.site.register(Schedule)
admin.site.register(ScheduleLog)
