# Table Header
# Module: Consumer Ops | Sub-Module : Meter Reading
# Table Type : Master (Global)
# Table Name : 2.3.8.3 Jobcard
# Description : Assigned and De-assigned record are created in this table consumer wise and month wise.
# Frequency of data changes : High
# Sample table : "Consumer Details monthly"
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


# Create Jobcard Table Start.

class Jobcard(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    meter_reader = models.IntegerField(null=True, blank=True)
    month = models.CharField(max_length=200, null=True, blank=True)
    bill_cycle = models.IntegerField(null=True, blank=True)
    route = models.IntegerField(null=True, blank=True)
    route_assigned = models.IntegerField(null=True, blank=True)
    assign_date = models.DateField(null=True, blank=True, default=datetime.now())
    status = models.IntegerField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted_for_mr = models.BooleanField(default=False)
    is_reading_completed = models.BooleanField(default=False)
    is_revisit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())


# Create Jobcard Table End.
