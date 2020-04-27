# table header
# module: Tenant | sub-module - Invoices, Payments
# table type : Master
# table name : 1.4 Tenant Invoices
# table description :  It will contain details for all invoices generated against the Tenant.
# frequency of data changes : High
# sample tale data : "Sub2","UTI4579989","8765675788","INV786965",
# reference tables : 1.1 Tenant Master
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Tenant Invoices table start.

class TenantInvoices(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    subscription_id = models.IntegerField(null=True, blank=True)
    tenantbankdetails_id = models.IntegerField(null=True, blank=True)
    invoice_number = models.CharField(max_length=200, blank=False, null=False)
    invoice_date = models.DateField(null=True, blank=True, default=datetime.now())
    invoice_amt = models.FloatField(null=True, blank=True)
    invoice_tax = models.FloatField(null=True, blank=True)
    invoice_url = models.CharField(max_length=200, blank=False, null=False)
    due_date = models.DateField(null=True, blank=True, default=datetime.now())
    contact_name = models.CharField(max_length=500, blank=False, null=False)
    contact_no = models.IntegerField(null=True, blank=True)
    email_id = models.CharField(max_length=200, blank=False, null=False)
    month = models.CharField(max_length=200, blank=False, null=False)
    billing_address = models.CharField(max_length=800, blank=False, null=False)
    address = models.CharField(max_length=500, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.invoice_number

    def __unicode__(self):
        return self.invoice_number

# Create Tenant Invoices table end.
