# table header
# module: Utility | sub-module - Utility Service
# table type : Master
# table name : 2.2.2  Utility Service Plan
# table description :  It will contain details for Utility Service Plan
# frequency of data changes : Low
# sample tale data : "Plan - A"
# reference tables : 2.1 Utility Master
# author : Gauri Deshmukh
# created on : 27/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Utility Service Plan table start.



class UtilityServicePlan(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    is_valid = models.BooleanField(default=False)
    validity = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    end_date = models.DateField(null=True, blank=True, default=datetime.now())
    location = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())


def __str__(self):
    return self.name


def __unicode__(self):
    return self.name


def get_utility_service_plan_by_id_string(id_string):
    return UtilityServicePlan.objects.get(id_string = id_string)


def get_utility_service_plan_by_id(id):
    return UtilityServicePlan.objects.get(id = id)
# Create  Utility Service Plan  table end.
