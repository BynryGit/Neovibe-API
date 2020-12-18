__author__ = "priyanka"

from django.contrib import admin
from v1.work_order.models.work_order_master import WorkOrderMaster
from v1.work_order.models.service_appointments import ServiceAppointment
from v1.work_order.models.work_order_assignment import WorkOrderAssignment

admin.site.register(WorkOrderMaster)
admin.site.register(ServiceAppointment)
admin.site.register(WorkOrderAssignment)
# Register your models here.
