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
from django.utils import timezone # importing package for datetime


# Create Utility Service Plan table start.



class UtilityServicePlan(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    category = models.BigIntegerField(null=True, blank=True) # CNG, PNG
    subcategory = models.BigIntegerField(null=True, blank=True) # Domestic, Industrial, Commercials
    type = models.BigIntegerField(null=True, blank=True) # prepaid, postpaid
    subtype = models.BigIntegerField(null=True, blank=True) # fixed, variable
    city = models.BigIntegerField(null=True, blank=True) # city1, city 2
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)


def __str__(self):
    return self.name


def __unicode__(self):
    return self.name


def get_utility_service_plan_by_id_string(id_string):
    try:
        return UtilityServicePlan.objects.get(id_string = id_string)
    except:
        return False


def get_utility_service_plan_by_id(id):
    try:
        return UtilityServicePlan.objects.get(id = id)
    except:
        return False


def get_utility_service_plans_by_dates(from_date, to_date, schedule):
    try:
        return UtilityServicePlan.objects.filter(utility=schedule.utility, start_date__lte=to_date, end_date__gte=from_date, is_active=True)
    except:
        return False
