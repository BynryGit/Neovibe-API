# table header
# module: Sourcing
# table type : Master
# table name : 2.5.10 SupplierPayment
# table description : A common Payment table that saves the Payment details wherever the payment details are required.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Payment Table start

class SupplierPayment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    payment_type = models.BigIntegerField(null=True, blank=True)
    invoice = models.BigIntegerField(null=True, blank=True)
    contract = models.BigIntegerField(null=True, blank=True)
    supplier = models.BigIntegerField(null=True, blank=True)
    supplier_financial = models.BigIntegerField(null=True, blank=True)
    demand = models.BigIntegerField(null=True, blank=True)
    invoice_amount = models.BigIntegerField(null=True, blank=True)
    paid_amount = models.BigIntegerField(null=True, blank=True)
    payment_mode = models.BigIntegerField(null=True, blank=True)
    cheque_no = models.BigIntegerField(null=True, blank=True)
    dd_no = models.BigIntegerField(null=True, blank=True)
    cheque_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    dd_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    txn_id = models.BigIntegerField(null=True, blank=True)
    account_no = models.CharField(max_length=200, blank=True, null=True)
    ifsc_code = models.CharField(max_length=200, blank=True, null=True)
    payment_source = models.BigIntegerField(null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    payment_status = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.txn_id)

    def __unicode__(self):
        return str(self.txn_id)

# Create Payment table end.


def get_supplier_payment_by_id(id):
    try:
        return SupplierPayment.objects.get(id = id)
    except:
        return False


def get_supplier_payment_by_id_string(id_string):
    try:
        return SupplierPayment.objects.get(id_string = id_string)
    except:
        return False


def get_contract_payment_by_id(id):
    try:
        return SupplierPayment.objects.get(id=id)
    except:
        return False


def get_contract_payment_by_id_string(id_string):
    try:
        return SupplierPayment.objects.get(id_string=id_string)
    except:
        return False