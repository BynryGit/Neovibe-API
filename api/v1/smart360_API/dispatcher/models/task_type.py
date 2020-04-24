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

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


# Create Task Type table start

<<<<<<< HEAD
# Create Task Type table start

=======
>>>>>>> b941903123e03248e891298e98bfc30481b8e0c9
class TaskType(models.Model):
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
<<<<<<< HEAD
        return self.task_type
# Create Task Type table end.
=======
        return self.name

# Create Task Type table end
>>>>>>> b941903123e03248e891298e98bfc30481b8e0c9
