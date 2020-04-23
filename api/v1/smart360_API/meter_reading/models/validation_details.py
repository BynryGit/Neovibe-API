# Table Header
# Module: Consumerops | Consumer Care
# Table Type : Master (Global)
# Table Name : 2.3.8.7 Validation Details
# Description :After submitting meter readings by meter reader, validation records(V1 and V2) will be created per reading.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Auther : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Validation Details Table Start.

class ValidationDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(null=True, blank=True)
    meter_reading_id = models.IntegerField(null=True, blank=True)
    month = models.CharField(null=True, blank=True)
    validation_type = models.IntegerField(null=True, blank=True)
    validator_id = models.IntegerField(null=True, blank=True)
    validator_meter_status = models.IntegerField(null=True, blank=True)
    validator_reader_status = models.IntegerField(null=True, blank=True)
    validator_reading = models.CharField(null=True, blank=True)
    validator_comment = models.CharField(null=True, blank=True)
    validator_image_remark = models.CharField(null=True, blank=True)
    validated_on = models.DateField(null=True, blank=True, default=datetime.now())
    is_meter_matching = models.BooleanField(default=False)
    is_reading_matching = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

# Create Validation Details Table End.
