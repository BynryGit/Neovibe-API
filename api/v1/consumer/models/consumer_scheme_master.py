# Table Header
# Module: Consumer Care |Sub-Module : Meter Reading, Billing
# Table Type : Master (Global)
# Table Name : 2.4.3. Consumer - Scheme master
# Description : This table will store all deposits or marketing scheme data associated with one Consumer
# Frequency of data changes : High
# Sample table : "EMI Scheme", "Deposit Scheme"
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Consumer Scheme Master Table Start.

class ConsumerSchemeMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    scheme_type = models.IntegerField(null=True, blank=True)  # TODO Conform for lookup Table
    scheme_name = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    effective_date = models.DateField(null=True, blank=True, default=datetime.now())
    expiry_date = models.DateField(null=True, blank=True, default=datetime.now())
    total_deposit_amt = models.FloatField(null=True, blank=True)
    scheme_tax_percentage = models.FloatField(null=True, blank=True)
    monthly_emi = models.FloatField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.scheme_name

    def __unicode__(self):
        return self.scheme_name

# Create Consumer Scheme Master table end.
