# table header
# module: billing | sub-module - billing
# table type : lookup (Local)
# table name : Tax
# table description : A lookup table for tax of given rate.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Tax Table
# author : Priyanka 
# created on : 01/03/2021

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database

# Create Tax table start.

class Tax(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    tax_name = models.CharField(max_length=200, blank=False, null=False)
    tax_percentage = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.tax_name

    def __unicode__(self):
        return self.tax_name

# Create Tax table end.

def get_tax_by_tenant_id_string(tenant_id_string):
    return Tax.objects.filter(tenant__id_string=tenant_id_string)

def get_tax_by_id_string(id_string):
    try:
        return Tax.objects.get(id_string = id_string)
    except:
        return False

def get_tax_by_id(id):
    try:
        return Tax.objects.get(id = id)
    except:
        return False