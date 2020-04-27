# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading
# Table Type : Master (Global)
# Table Name : 2.3.8.6 Reading Additional parameters
# Description :Additional information will be saved in this table reading wise.
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


# Create Reading Additional Parameters Table Start

class ReadingAdditionalParameters(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    meter_reading = models.IntegerField(null=True, blank=True)
    lat = models.CharField(max_length=200, null=True, blank=True)
    long = models.CharField(max_length=200, null=True, blank=True)
    new_sequence = models.CharField(max_length=500, null=True, blank=True)
    prev_sequence = models.CharField(max_length=500, null=True, blank=True)
    location_guidance = models.CharField(max_length=500, null=True, blank=True)
    time_taken = models.CharField(max_length=200, null=True, blank=True)

    extra_parameter = models.IntegerField(null=True, blank=True)
    extra_parameter_remark = models.CharField(max_length=500, null=True, blank=True)
    parameter_flag_type = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

# Create Reading Additional Parameters Table end
