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
from datetime import datetime # importing package for datetime

from django.db import models  # importing package for database

# Create Department table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class Department(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
# Create Department table end


def get_department_by_tenant_id_string(id_string):
    return Department.objects.filter(tenant__id_string=id_string)


def get_department_by_id_string(id_string):
    return Department.objects.filter(id_string=id_string)


def get_department_by_id(id):
    return Department.objects.filter(id=id)