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
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Tenant Invoice Transaction table start.

class TenantInvoiceTransaction(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    invoice_number = models.IntegerField(null=True, blank=True)
    payment_method = models.CharField(max_length=200, blank=False, null=False)
    payment_channel = models.CharField(max_length=200, blank=False, null=False)
    transaction_no = models.CharField(max_length=200, blank=False, null=False)
    transaction_date = models.DateField(null=True, blank=True, default=datetime.now())
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    currency = models.CharField(max_length=100, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.invoice_number

    def __unicode__(self):
        return self.invoice_number

# Create Tenant Invoice Transaction table end.
