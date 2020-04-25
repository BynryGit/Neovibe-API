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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Tenant Invoice Transaction table start.

class TenantInvoiceTransaction(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    invoice_number = models.IntegerField(null=True, blank=True)
    payment_method = models.CharField(max_length=200, blank=False, null=False)
    plan_id = models.IntegerField(null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    currenecy = models.CharField(max_length=100, blank=False, null=False)
    account_id  = models.CharField(max_length=200, blank=False, null=False)
    account_holder_name  = models.CharField(max_length=300, blank=False, null=False)
    account_number  = models.CharField(max_length=200, blank=False, null=False)
    billing_status  = models.CharField(max_length=100, blank=False, null=False)
    outstanding = models.FloatField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True, default=datetime.now())
    month  = models.CharField(max_length=100, blank=False, null=False)
    is_emi = models.BooleanField(default=False)
    emi = models.FloatField(null=True, blank=True)
    is_penalty = models.BooleanField(default=False)
    penalty = models.FloatField(null=True, blank=True)
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
