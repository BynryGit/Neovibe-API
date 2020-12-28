__author__ = "priyanka"

from django.contrib import admin
from v1.work_order.models.work_order_master import WorkOrderMaster
from v1.work_order.models.service_appointments import ServiceAppointment
from v1.work_order.models.work_order_assignment import WorkOrderAssignment
from v1.work_order.models.work_order_rules import WorkOrderRule
from v1.work_order.models.service_appointment_status import ServiceAppointmentStatus

admin.site.register(WorkOrderMaster)
admin.site.register(ServiceAppointment)
admin.site.register(WorkOrderAssignment)
admin.site.register(WorkOrderRule)
admin.site.register(ServiceAppointmentStatus)
# Register your models here.
