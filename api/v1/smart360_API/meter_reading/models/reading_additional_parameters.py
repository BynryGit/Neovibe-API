# Table Header
# Module: Consumerops | Consumer Care
# Table Type : Master (Global)
# Table Name : 2.3.8.6 Reading Additional parameters
# Description :Additional information will be saved in this table reading wise.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Auther : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Meter Reading Additional Parameter Table Start.

class ReadingAdditionalParameters(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(null=True, blank=True)
    meter_reading_id = models.IntegerField(null=True, blank=True)
    lat = models.CharField(null=True, blank=True)
    long = models.CharField(null=True, blank=True)
    new_sequence = models.CharField(null=True, blank=True)
    prev_sequence = models.CharField(null=True, blank=True)
    location_guidance = models.CharField(null=True, blank=True)
    time_taken = models.CharField(null=True, blank=True)
    reading_type_id = models.IntegerField(null=True, blank=True)
    reading_type_status_id = models.IntegerField(null=True, blank=True)
    extra_parameter_id = models.IntegerField(null=True, blank=True)
    extra_parameter_remark = models.CharField(null=True, blank=True)
    parameter_flag_type = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

# Create Reading Additional parameter Table End.