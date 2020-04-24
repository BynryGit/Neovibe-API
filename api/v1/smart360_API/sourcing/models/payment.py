# table header
# module: Sourcing
# table type : Master
# table name : 2.5.10 Payment
# table description : This is a common Payment table that saves the Payment details wherever the payment details are required.
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


# Create Payment Table start

class Payment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    payment_type_id = models.IntegerField(null=True, blank=True)
    invoice_id = models.IntegerField(null=True, blank=True)
    contract_id = models.IntegerField(null=True, blank=True)
    supplier_id = models.IntegerField(null=True, blank=True)
    supplier_financial_id = models.IntegerField(null=True, blank=True)
    demand_id = models.IntegerField(null=True, blank=True)
    invoice_amount = models.IntegerField(null=True, blank=True)
    paid_amount = models.IntegerField(null=True, blank=True)
    payment_mode_id = models.IntegerField(null=True, blank=True)
    cheque_no = models.IntegerField(null=True, blank=True)
    dd_no = models.IntegerField(null=True, blank=True)
    cheque_date = models.DateField(null=True, blank=True, default=datetime.now())
    dd_date = models.DateField(null=True, blank=True, default=datetime.now())
    bank_name_id = models.IntegerField(null=True, blank=True)
    txn_id = models.IntegerField(null=True, blank=True)
    account_no = models.CharField(max_length=200, blank=True, null=True)
    ifsc = models.CharField(max_length=200, blank=True, null=True)
    payment_source_id = models.IntegerField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True, default=datetime.now())
    payment_status = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

# Create Payment table end.