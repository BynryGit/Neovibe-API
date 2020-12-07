# Table Header
# Module: Consumer Ops | Sub-Module : Meter Reading
# Table Type : Master (Global)
# Table Name : 2.4.12. Smart Meter Data
# Description : It is Smart Meter Data table. It will contain the list of Smart Metering data details.
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


# Create Smart Meter Data Table Start

class SmartMeterData(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    meter = models.BigIntegerField(null=True, blank=True)
    meter_reading = models.CharField(max_length=200, null=True, blank=True)
    meter_status = models.BigIntegerField(null=True, blank=True)
    route = models.BigIntegerField(null=True, blank=True)
    data_vendor_no = models.CharField(max_length=200, null=True, blank=True)
    reading_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.consumer_id)

    def __unicode__(self):
        return str(self.consumer_id)

# Create Smart Meter Data Table end
