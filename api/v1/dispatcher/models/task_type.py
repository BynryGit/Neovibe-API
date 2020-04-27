# Table Header
# module: O&M  | sub-module - SOP
# Table Type : Lookup (Local)
# Table Name : 2.12.77 Task Type (Local)
# Description : A lookup table for types of task added in SOP's.
# Frequency of data changes : Low
# Sample Table Data : Image, Parameter, Material
# Reference Table : 2.6.3 SOP Master Details
# Author : Jayshree Kumbhare
# Creation Date : 22-04-2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Task Type table start

class TaskType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
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

# Create Task Type table end
