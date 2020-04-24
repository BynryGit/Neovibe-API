# Table Header
# Module: Consumerops | Consumer Care
# Table Type : Master (Global)
# Table Name : 2.3.8.4 Meter Reading
# Description : When meter takes the reading and upload on server, entry will be created in meter reading table.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Meter Reading Table Start.

class MeterReading(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(null=True, blank=True)
    jobcard_id = models.IntegerField(null=True, blank=True)
    bill_cycle_id = models.IntegerField(null=True, blank=True)
    mru_id = models.IntegerField(null=True, blank=True)
    meter_status_id = models.IntegerField(null=True, blank=True)
    reader_status_id = models.IntegerField(null=True, blank=True)
    reading_img_id = models.IntegerField(null=True, blank=True)
    month = models.CharField(null=True, blank=True)
    current_reading = models.CharField(null=True, blank=True)
    reading_date = models.DateField(null=True, blank=True, default=datetime.now())
    reading_status_id = models.IntegerField(null=True, blank=True)
    suspicious_activity = models.BooleanField(default=False)
    is_qr_tempered = models.BooleanField(default=False)
    reading_taken_by = models.IntegerField(null=True, blank=True)
    is_solar_meter = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_account_verified = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

# Create Meter Reading Table End.