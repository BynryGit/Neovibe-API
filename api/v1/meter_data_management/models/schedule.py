__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Schedule
# Description : It is schedule table. This table will save all the schedules.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 06/01/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from datetime import datetime # importing package for datetime
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.contrib.postgres.fields import JSONField


# Create Schedule Table Start

class Schedule(models.Model):
    SCHEDULE_STATUS = (
        (0, 'PENDING'),
        (1, 'COMPLETED'),
        (2, 'INPROGRESS'),
    )

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    read_cycle_id = models.BigIntegerField(null=False, blank=False)
    activity_type_id = models.BigIntegerField(null=False, blank=False)
    frequency_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    repeat_every = models.CharField(max_length=200, blank=True, null=True)
    occurs_on = JSONField(default=[])
    schedule_status = models.IntegerField(choices=SCHEDULE_STATUS, default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    @property
    def get_read_cycle_name(self):
        read_cycle = get_read_cycle_by_id(self.read_cycle_id)
        return read_cycle

    @property
    def get_activity_type(self):
        activity_type = get_global_lookup_by_id(self.activity_type_id)
        return activity_type

    @property
    def get_frequency_name(self):
        frequency = get_global_lookup_by_id(self.frequency_id)
        return frequency

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return str(self.id_string)

# Create Schedule Table end


def get_schedule_by_id(id):
    try:
        return Schedule.objects.get(id=id, is_active=True)
    except:
        return False


def get_schedule_by_id_string(id_string):
    try:
        return Schedule.objects.get(id_string=id_string, is_active=True)
    except:
        return False


def get_all_schedules():
    return Schedule.objects.all(is_active=True)