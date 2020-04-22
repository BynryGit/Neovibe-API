# Table Header : Schedule Status
# Table Type : Lookup (Local)
# Table Name : 2.12.51 Schedule Type
# Description : This table store the schedule status with respect to particular schedule.
# Sample Table Data : Conform, Reject, Pending
# Frequency of data changes : Low
# Reference Table : 2.3.8.1 Schedule
# Auther : Jayshree
# Creation Date : 22/04/2020

import datetime
import uuid
from django.db import models

# Start the Code
class ScheduleStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    schedule_status = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.schedule_status

    def __unicode__(self):
        return self.schedule_status
# End the Code