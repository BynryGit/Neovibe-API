# Table Header : Task Type
# module: O&M  | sub-module - SOP
# Table Type : Lookup (Local)
# Table Name : 2.12.77 Task Type (Local)
# Description : A lookup table for types of task added in SOP's.
# Frequency of data changes : Low
# Sample Table Data : Image, Parameter, Material
# Reference Table : 2.6.3 SOP Master Details
# Author : Jayshree
# Creation Date : 22-04-2020

import datetime
import uuid
from django.db import models

# Start the Code
class TaskType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    task_type = models.CharField(max_length=40, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.task_type

    def __unicode__(self):
        return self.task_type
# End The Code