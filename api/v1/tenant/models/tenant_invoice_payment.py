# table header
# module: Tenant | sub-module - Invoices, Payments
# table type : Master
# table name : 1.6  Tenant Invoice Payment
# table description :  It will contain details for all invoices transaction for multiple invoice references.
# frequency of data changes : High
# sample tale data :"P124","$27","acc546786"
# reference tables : 1.4 Tenant Invoices, 1.5. Tenant Invoice Transaction
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_invoice import get_tenant_invoice_by_id
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database


# Create Tenant Invoice Transaction table start.

class TenantInvoicePayment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    invoice_id = models.BigIntegerField(null=True, blank=True)
    payment_method = models.CharField(max_length=200, blank=True, null=True)
    payment_channel = models.CharField(max_length=200, blank=True, null=True)
    transaction_no = models.CharField(max_length=200, blank=True, null=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    tax_amount = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return str(self.invoice_id)

    def __unicode__(self):
        return str(self.invoice_id)

    @property
    def get_invoice_id(self):
        tenant_invoice = get_tenant_invoice_by_id(self.invoice_id)
        return tenant_invoice

# Create Tenant Invoice Transaction table end.


def get_tenant_invoice_payment_by_id(id):
    try:
        return TenantInvoicePayment.objects.get(id=id)
    except:
        return False


def get_tenant_invoice_payment_by_id_string(id_string):
    try:
        return TenantInvoicePayment.objects.get(id_string=id_string)
    except:
        return False
