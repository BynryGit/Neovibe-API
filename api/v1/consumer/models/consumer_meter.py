# Table Header
# Module: Consumer Care | Sub-Module : Meter Reading, Billing
# Table Type : Master (Global)
# Table Name : 2.4.7. Consumer - Meter
# Description : It will save all active and inactive consumers and associated meters for given tenant.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Consumer Meter Table Start.

class ConsumerMeter(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer = models.IntegerField(null=True, blank=True)
    meter = models.IntegerField(null=True, blank=True)
    assign_date = models.DateField(null=True, blank=True, default=datetime.now())
    initial_reading = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.meter_id) + '-' + str(self.consumer_id) + '-' + str(self.assign_date) + '-' + str(
            self.initial_reading) + '-' + str(self.status)

# Create Consumer meter table end.
