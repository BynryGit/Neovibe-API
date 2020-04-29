# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master (Global)
# Table Name : 2.3.8.1 Schedule
# Description : It is schedule table. This table will save all the schedules month wise and cycle wise.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Schedule Table Start

class Schedule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    schedule_type = models.BigIntegerField(null=True, blank=True) #Meter Reading, Bill Distribution, Notices
    activity_type = models.BigIntegerField(null=True, blank=True) #Manual, Photo, SpotBill, SmartMeter
    bill_cycle = models.BigIntegerField(null=True, blank=True)
    bill_month = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    end_date = models.DateField(null=True, blank=True, default=datetime.now())
    due_date = models.DateField(null=True, blank=True, default=datetime.now())
    schedule_status = models.BigIntegerField(null=True, blank=True)
    is_valid_next_cycle = models.BooleanField(default=False)
    is_imported = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.bill_cycle

    def __unicode__(self):
        return self.bill_cycle

# Create Schedule Table end
