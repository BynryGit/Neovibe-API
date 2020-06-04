# table header
# module: Tenant | sub-module - Invoices, Payments
# table type : Master
# table name : 1.4 Tenant Invoice
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
from django.db import models  # importing package for database
from v1.tenant.models.tenant_bank_details import get_tenant_bank_details_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.tenant.models.tenant_subscription import get_tenant_subscription_by_id


# Create Tenant Invoices table start.


class TenantInvoice(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    tenant_subscription_id = models.BigIntegerField(null=True, blank=True)
    tenant_bank_detail_id = models.BigIntegerField(null=True, blank=True)
    invoice_number = models.CharField(max_length=200, blank=False, null=False)
    invoice_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    invoice_amt = models.FloatField(null=True, blank=True)
    invoice_tax = models.FloatField(null=True, blank=True)
    invoice_url = models.CharField(max_length=200, blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    contact_name = models.CharField(max_length=500, blank=True, null=True)
    contact_no = models.BigIntegerField(null=True, blank=True)
    email_id = models.CharField(max_length=200, blank=False, null=False)
    month = models.CharField(max_length=200, blank=True, null=True)
    billing_address = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.invoice_number

    def __unicode__(self):
        return self.invoice_number

    @property
    def get_tenant_subscription_id(self):
        tenant_subscription = get_tenant_subscription_by_id(self.tenant_subscription_id)
        return tenant_subscription

    @property
    def get_tenant_bank_detail_id(self):
        tenant_bank = get_tenant_bank_details_by_id(self.tenant_bank_detail_id)
        return tenant_bank

# Create Tenant Invoices table end.


def get_tenant_invoice_by_id(id):
    try:
        return TenantInvoice.objects.get(id=id)
    except:
        return False


def get_tenant_invoice_by_id_string(id_string):
    try:
        return TenantInvoice.objects.get(id_string=id_string)
    except:
        return False
