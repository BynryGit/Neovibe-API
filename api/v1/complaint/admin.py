from django.contrib import admin
from v1.complaint.models.complaint import Complaint
from v1.complaint.models.complaint_assignment import ComplaintAssignment

admin.site.register(Complaint)
admin.site.register(ComplaintAssignment)