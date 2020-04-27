# table header
# module: Sourcing
# table type : Master
# table name : 2.5.10 Payment
# table description : A common Payment table that saves the Payment details wherever the payment details are required.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database

from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster


# Create Payment Table start

class Payment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    payment_type = models.IntegerField(null=True, blank=True)
    invoice = models.IntegerField(null=True, blank=True)
    contract = models.IntegerField(null=True, blank=True)
    supplier = models.IntegerField(null=True, blank=True)
    supplier_financial = models.IntegerField(null=True, blank=True)
    demand = models.IntegerField(null=True, blank=True)
    invoice_amount = models.IntegerField(null=True, blank=True)
    paid_amount = models.IntegerField(null=True, blank=True)
    payment_mode = models.IntegerField(null=True, blank=True)
    cheque_no = models.IntegerField(null=True, blank=True)
    dd_no = models.IntegerField(null=True, blank=True)
    cheque_date = models.DateField(null=True, blank=True, default=datetime.now())
    dd_date = models.DateField(null=True, blank=True, default=datetime.now())
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    txn_id = models.IntegerField(null=True, blank=True)
    account_no = models.CharField(max_length=200, blank=True, null=True)
    ifsc_code = models.CharField(max_length=200, blank=True, null=True)
    payment_source = models.IntegerField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True, default=datetime.now())
    payment_status = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.invoice

    def __unicode__(self):
        return self.invoice

# Create Payment table end.
