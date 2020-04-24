# Table Header
# Table Type : Lookup (Local)
# Table Name : 2.12.56 Reading Taken By
# Description : It Reading Taken By and ID of Reading Taken By to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : "Manual" , "Smart meter"
# Reference Table : 2.3.8.4 Meter Reading
# Author : Jayshree Kumbhare
# Creation Date : 22-04-2020

# change history
# <ddmmyyyy>-<changes>-<Author>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


# Create Reading Taken By table start

class ReadingTakenBy(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Reading Taken By table end
