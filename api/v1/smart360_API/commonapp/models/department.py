# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name : 2.12.16 Department
# Description : It is a global lookup table that will store various departments
# Frequency of data changes : Low
# Sample Table Data : "Marketing" , "Finance" , "Operation Management".
# Reference Table : 2.7.1. Employee, 2.7.5. Employee_Positions, 2.5.1. User Details.
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Department table start
class Department(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
# Create Department table end
