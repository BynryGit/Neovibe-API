# Table Header
# Module: Consumerops | Consumer Care
# Table Type : Master (Global)
# Table Name : 2.3.8.1 Schedule
# Description : It is schedule table. This table will save all the schedules month wise and cycle wise.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Schedule Table Start.

class Schedule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    schedule_type = models.IntegerField(null=True, blank=True)
    activity_type = models.IntegerField(null=True, blank=True)
    bill_cycle_id = models.IntegerField(null=True, blank=True)
    month = models.CharField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    end_date = models.DateField(null=True, blank=True, default=datetime.now())
    due_date = models.DateField(null=True, blank=True, default=datetime.now())
    schedule_status = models.IntegerField(null=True, blank=True)
    is_valid_next_cycle = models.BooleanField(default=False)
    is_imported = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

# Create Schedule Table End.