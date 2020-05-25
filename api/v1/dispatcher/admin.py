from django.contrib import admin
from v1.dispatcher.models.closure_report import ClosureReport
from v1.dispatcher.models.closure_report_transaction import ClosureReportTransaction
from v1.dispatcher.models.service_type import ServiceTypes
from v1.dispatcher.models.service_appointments import ServiceRequest
from v1.dispatcher.models.service_assignment import ServiceAssignment
from v1.dispatcher.models.sop_assign import ServiceAssign
from v1.dispatcher.models.sop_master import SopMaster
from v1.dispatcher.models.sop_master_details import SopMasterDetails
from v1.dispatcher.models.sop_status import SopStatus
from v1.dispatcher.models.task_type import TaskType

admin.site.register(ClosureReport)
admin.site.register(ClosureReportTransaction)
admin.site.register(ServiceTypes)
admin.site.register(ServiceRequest)
admin.site.register(ServiceAssignment)
admin.site.register(SopMaster)
admin.site.register(SopMasterDetails)
admin.site.register(SopStatus)
admin.site.register(TaskType)
