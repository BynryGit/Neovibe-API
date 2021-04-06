# table header
# module: billing | sub-module - billing
# table type : lookup (Local)
# table name : Bill Invoice Section 
# table description : A lookup table for  Bill Invoice Section of given Bill.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Bill Invoice Section Table
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

# Create Bill Invoice Section table start.

class BillInvoiceSection(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    section_key = models.CharField(max_length=200, null=True, blank=True)
    section = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.section_key

    def __unicode__(self):
        return self.section_key

# Create Bill Invoice Section table end.


def get_bill_invoice_section_by_id_string(id_string):
    try:
        return BillInvoiceSection.objects.get(id_string = id_string)
    except:
        return False

def get_bill_invoice_section_by_id(id):
    try:
        return BillInvoiceSection.objects.get(id = id)
    except:
        return False