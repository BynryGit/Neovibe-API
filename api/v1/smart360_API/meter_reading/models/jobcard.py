# Table Header
# Module: Consumerops | Consumer Care
# Table Type : Master (Global)
# Table Name : 2.3.8.3 Jobcard
# Description : Assigned and Deassigned record are created in this table consumer wise and month wise.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Auther : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Jobcard Table Start.

class Jobcard(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(null=True, blank=True)
    bill_cycle_id = models.IntegerField(null=True, blank=True)
    mru_id = models.IntegerField(null=True, blank=True)
    route_assigned_id = models.IntegerField(null=True, blank=True)
    meter_reader_id = models.IntegerField(null=True, blank=True)
    month = models.CharField(null=True, blank=True)
    assign_date = models.DateField(null=True, blank=True, default=datetime.now())
    status_id = models.IntegerField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted_for_mr = models.BooleanField(default=False)
    is_reading_completed = models.BooleanField(default=False)
    is_revisit = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

# Create Jobcard Table End.