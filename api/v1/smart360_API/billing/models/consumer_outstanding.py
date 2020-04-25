# Table Header
# Module: Consumer Care | Sub-Module : Billing
# Table Type : Master (Global)
# Table Name : 2.4.11. Consumer - Outstanding
# Description : It will contain the amount outstanding against consumer with outstanding days and paid amount records.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Consumer OutStanding Table Start.

class ConsumerOutstanding(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer = models.IntegerField(null=True, blank=True)
    outstanding_amt = models.FloatField(blank=False, null=False)
    city = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.consumer_id) + '-' + str(self.outstanding)

# Create Consumer Outstanding table end.
