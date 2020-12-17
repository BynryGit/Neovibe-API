__author__ = "priyanka"

from django.contrib import admin
from v1.work_order.models.service_master import ServiceMaster
from v1.work_order.models.service_appointments import ServiceAppointment
from v1.work_order.models.service_assignment import ServiceAssignment

admin.site.register(ServiceMaster)
admin.site.register(ServiceAppointment)
admin.site.register(ServiceAssignment)
# Register your models here.
