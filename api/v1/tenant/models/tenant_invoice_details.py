# table header
# module: Tenant | sub-module - Invoices, Payments
# table type : Master
# table name : 1.5  Tenant Invoice Transaction
# table description :  It will contain details for all invoices transaction for multiple invoice references.
# frequency of data changes : High
# sample tale data :"INV675","Rs.4500","23",
# reference tables : 1.4 Tenant Invoices
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Tenant Invoice Transaction table start.

class TenantInvoiceDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    tenantinvoices_id = models.BigIntegerField(null=True, blank=True)
    invoice_number = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=500, blank=False, null=False)
    qty = models.FloatField(null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.invoice_number

    def __unicode__(self):
        return self.invoice_number

# Create Tenant Invoice Transaction table end.
