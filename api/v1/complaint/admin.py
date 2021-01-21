from django.contrib import admin
from v1.complaint.models.complaint import Complaint
from v1.complaint.models.complaint_assignment import ComplaintAssignment
from v1.complaint.models.consumer_complaint_master import ConsumerComplaintMaster

admin.site.register(Complaint)
admin.site.register(ComplaintAssignment)
admin.site.register(ConsumerComplaintMaster)