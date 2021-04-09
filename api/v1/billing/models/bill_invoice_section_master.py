# table header
# module: billing | sub-module - billing
# table type : Master
# table name : Bill Invoice Section Master
# table description : A lookup table for  Bill Invoice Section Master of given Bill.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Bill Invoice Section Master Table
# author : Priyanka 
# created on : 06/04/2021

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from django.contrib.postgres.fields import JSONField

# Create Bill Invoice Section table start.

class BillInvoiceSectionMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    sections = JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.id_string

    def __unicode__(self):
        return self.id_string

# Create Bill Invoice Section table end.


def get_bill_invoice_section_master_by_id_string(id_string):
    try:
        return BillInvoiceSectionMaster.objects.get(id_string = id_string)
    except:
        return False

def get_bill_invoice_section_master_by_id(id):
    try:
        return BillInvoiceSectionMaster.objects.get(id = id)
    except:
        return False