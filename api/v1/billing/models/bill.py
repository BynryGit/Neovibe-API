# table header
# module: billing | sub-module - billing
# table type : lookup (Local)
# table name : Bill Master
# table description : A lookup table for  Bill  of given Bill.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Bill Master Table
# author : Priyanka 
# created on : 01/03/2021

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database

from django.contrib.postgres.fields import JSONField
import fsm
from django.utils import timezone # importing package for datetime

# Create Bill Master table start.

class Bill(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_service_contract_detail_id = models.BigIntegerField(null=True, blank=True)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    bill_month = models.CharField(max_length=200, blank=False, null=False)
    bill_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    bill_period = models.CharField(max_length=200, blank=False, null=False)
    meter_reading = JSONField(default=[])
    rate_details = JSONField(default=[])
    additional_charges = JSONField(default=[])
    opening_balance = models.CharField(max_length=200, blank=False, null=False)
    current_charges = models.CharField(max_length=200, blank=False, null=False)
    bill_frequency_id = models.BigIntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_adjusted = models.BooleanField(default=False)
    is_spot_bill = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.consumer_service_contract_detail_id

    def __unicode__(self):
        return self.consumer_service_contract_detail_id

# Create Bill Master table end.

def get_bill_by_tenant_id_string(tenant_id_string):
    return Bill.objects.filter(tenant__id_string=tenant_id_string)

def get_bill_by_id_string(id_string):
    try:
        return Bill.objects.get(id_string = id_string)
    except:
        return False

def get_bill_by_id(id):
    try:
        return Bill.objects.get(id = id)
    except:
        return False