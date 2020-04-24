# Table Header
# Module: Consumerops | Consumer Care
# Table Type : Master (Global)
# Table Name : 2.3.8.5 Meter Reading Images
# Description : It is meter reading images table for saving images readingwise.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Auther : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Meter Reading Images Table Start.

class MeterReadingImages(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(null=True, blank=True)
    meter_reading_id = models.IntegerField(null=True, blank=True)
    type_id = models.IntegerField(null=True, blank=True)
    image_url = models.UrlField(null=False, blank=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

# Create Meter Reading Images Table End.