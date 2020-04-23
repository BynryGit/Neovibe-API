# table header
# module: Consumer care & Ops | sub-module - Consumer, Metering, Billing
# Table Type : Lookup (local)
# Table Name : 2.12.23 Bill Cycle
# Description : Bill Cycle and ID of Bill Cycle to be used by Operator or Utility.
# Frequency of data changes : Medium
# Sample Table Data : 15,16,17,18, 21,22,23,24,00
# Reference Table : 2.3.1. Consumer Master, 2.3.9 Invoice/Bill, 2.3.8.3 Jobcard, 2.3.8.4 Meter Reading,
#                   2.3.8.1 Schedule, 2.3.8.2 Reading Consumer Master, Smart Meter Reading, Smart Meter Billing
# Author : Jayshree Kumbhare
# Creation Date : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Bill Cycle table start

class BillCycle(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    code = models.IntegerField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

# Create Bill Cycle table end
