# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading , Validation
# Table Type : Master (Global)
# Table Name : 2.3.8.5 Meter Reading Images
# Description : It is meter reading images table for saving images readingwise.
# Frequency of data changes : High
# Sample table : "Meter Images"
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


# Create Meter Reading Table Start

class MeterReadingImages(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(null=True, blank=True)
    meter_reading = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    image_url = models.UrlField(null=False, blank=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

# Create Meter Reading Images Table End
