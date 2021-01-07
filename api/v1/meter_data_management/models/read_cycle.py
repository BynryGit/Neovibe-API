__author__ = "aki"

# table header
# module: Consumer care & Ops | sub-module - Consumer, Metering, Billing
# Table Type : Lookup (local)
# Table Name :
# Description : Used to save read cycle according to utility.
# Frequency of data changes : Medium
# Sample Table Data : 15,16,17,18, 21,22,23,24,00
# Reference Table : 2.3.1. Consumer Master, 2.3.9 Invoice/Bill, 2.3.8.3 Jobcard, 2.3.8.4 Meter Reading,
#                   2.3.8.1 Schedule, 2.3.8.2 Reading Consumer Master, Smart Meter Reading, Smart Meter Billing
# Author : Akshay Nibrad
# Creation Date : 06/01/2021

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Read Cycle table start

class ReadCycle(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    city_id = models.BigIntegerField(null=False, blank=False)
    zone_id = models.BigIntegerField(null=True, blank=True)
    division_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    subarea_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Read Cycle table end


def get_read_cycle_by_id(id):
    try:
        return ReadCycle.objects.get(id=id)
    except:
        return False


def get_read_cycle_by_id_string(id_string):
    try:
        return ReadCycle.objects.get(id_string=id_string)
    except:
        return False
