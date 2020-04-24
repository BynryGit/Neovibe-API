# Table Header : Schedule Type
# Table Type : Lookup (Local)
# Table Name : 2.12.51 Schedule Type
# Description : It Schedule type and ID of various Schedule type to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : Reading, Billing
# Reference Table : 2.3.8.1 Schedule
# Author : Jayshree
# Creation Date : 22/04/2020

import datetime
import uuid
from django.db import models

# Start the Code

class ScheduleType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    schedule_type = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.schedule_type

    def __unicode__(self):
        return self.schedule_type
# End the Code