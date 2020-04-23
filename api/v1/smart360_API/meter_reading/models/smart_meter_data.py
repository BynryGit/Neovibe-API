# Table Header
# Module: Consumerops | Consumer Care
# Table Type : Master (Global)
# Table Name : 2.4.12. Smart Meter Data
# Description : It is Smart Meter Data table. It will contain the list of Smart Metering data details.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Auther : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Smart Meter Data Table Start.

class SmartMeterData(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_id = models.IntegerField(null=True, blank=True)
    meter_id = models.IntegerField(null=True, blank=True)
    meter_reading = models.CharField(null=True, blank=True)
    meter_status = models.IntegerField(null=True, blank=True)
    router_id = models.IntegerField(null=True, blank=True)
    data_vendor_no = models.CharField(null=True, blank=True)
    reading_date = models.DateField(null=True, blank=True, default=datetime.now())
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

# Create Smart Meter Data Table End.