# Table Header
# Module: Consumer Care & Ops | Sub-Module : Validation
# Table Type : Master (Global)
# Table Name : 2.3.8.7 Validation Details
# Description : After submitting meter readings by meter reader, v1 and v2 records will be created per reading.
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


# Create Validation Details Table Start

class ValidationDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    meter_reading = models.BigIntegerField(null=True, blank=True)
    month = models.CharField(max_length=200, null=True, blank=True)
    validation_type = models.BigIntegerField(null=True, blank=True)
    validator = models.BigIntegerField(null=True, blank=True)
    validator_meter_status = models.BigIntegerField(null=True, blank=True)
    validator_reader_status = models.BigIntegerField(null=True, blank=True)
    validator_reading = models.CharField(max_length=200, null=True, blank=True)
    validator_comment = models.CharField(max_length=500, null=True, blank=True)
    validator_image_remark = models.CharField(max_length=500, null=True, blank=True)
    validated_on = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_meter_matching = models.BooleanField(default=False)
    is_reading_matching = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

# Create Validation Details Table end

