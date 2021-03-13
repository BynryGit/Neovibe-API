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
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Consumer Scheme Master Table Start.

class ConsumerSchemeMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    scheme_type_id = models.BigIntegerField(null=True, blank=True)  # TODO Conform for lookup Table
    scheme_name = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    effective_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    expiry_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    total_deposit_amt = models.FloatField(null=True, blank=True)
    scheme_tax_percentage = models.FloatField(null=True, blank=True)
    monthly_emi = models.FloatField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.scheme_name

    def __unicode__(self):
        return self.scheme_name


def get_scheme_by_id_string(id_string):
    try:
        return ConsumerSchemeMaster.objects.get(id_string = id_string)
    except:
        return False


def get_scheme_by_id(id):
    try:
        return ConsumerSchemeMaster.objects.get(id = id)
    except:
        return False

# Create Consumer Scheme Master table end.
