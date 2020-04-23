# Table Header
# module: Consumer care & Ops | sub-module - Consumer, Metering, Billing
# Table Type : Lookup (Local)
# Table Name : 2.12.24 MRU
# Description : MRU and ID of MRU to be used by Operator or Utility
# Frequency of data changes : Medium
# Sample Table Data : "1517" , "1618"
# Reference Table : 2.3.1. Consumer Master
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create MRU table start
class MRU(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    code = models.CharField(max_length=200, blank=False, null=False)
    mru_token = models.IntegerField(blank=False, null=False)
    bill_cycle = models.IntegerField(blank=False, null=False)
    month = models.CharField(max_length=200, blank=False, null=False)
    mru_data = models.FileField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code
# Create MRU table end
