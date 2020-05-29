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
from v1.meter_reading.models.activity_type import get_activity_type_by_id
from v1.meter_reading.models.schedule_type import get_schedule_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Schedule Table Start

class Schedule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    schedule_type_id = models.BigIntegerField(null=True, blank=True) #Meter Reading, Bill Distribution, Notices
    activity_type_id = models.BigIntegerField(null=True, blank=True) #Manual, Photo, SpotBill, SmartMeter
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    bill_month = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    end_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    due_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    schedule_status_id = models.BigIntegerField(null=True, blank=True)
    is_valid_next_cycle = models.BooleanField(default=False)
    is_imported = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    @property
    def get_schedule_type(self):
        schedule_type = get_schedule_type_by_id(self.schedule_type_id)
        return schedule_type

    @property
    def get_activity_type(self):
        activity_type = get_activity_type_by_id(self.activity_type_id)
        return activity_type

    def __str__(self):
        return self.bill_cycle

    def __unicode__(self):
        return self.bill_cycle

# Create Schedule Table end

def get_all_schedules():
    return Schedule.objects.all()