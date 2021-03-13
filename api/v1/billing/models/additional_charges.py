# table header
# module: billing | sub-module - billing
# table type : lookup (Local)
# table name : Additional Charges
# table description : A lookup table for  Additional Charges of given Bill.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Additional Charges Table
# author : Priyanka 
# created on : 01/03/2021

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime

# Create Additional Charges table start.

class AdditionalCharges(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_charges = models.CharField(max_length=200, blank=False, null=False)
    adjustment_amount = models.CharField(max_length=200, blank=False, null=False)
    penalty_charges = models.CharField(max_length=200, blank=False, null=False)
    discount_amount = models.CharField(max_length=200, blank=False, null=False)
    EMI = models.CharField(max_length=200, blank=False, null=False)
    rental_charges = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.service_charges

    def __unicode__(self):
        return self.service_charges

# Create Additional Charges table end.

def get_additional_charges_by_tenant_id_string(tenant_id_string):
    return AdditionalCharges.objects.filter(tenant__id_string=tenant_id_string)

def get_additional_charges_by_id_string(id_string):
    try:
        return AdditionalCharges.objects.get(id_string = id_string)
    except:
        return False

def get_additional_charges_by_id(id):
    try:
        return AdditionalCharges.objects.get(id = id)
    except:
        return False