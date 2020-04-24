# table header
# module: Sourcing
# table type : Master
# table name : 2.5.9 Invoice
# table description : The Invoice table saves the Invoice details of Supplier or Contract
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
from decimal import Decimal   # importing package for float number

# Create Invoice Table start

class Invoice(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    contract_id = models.IntegerField(null=True, blank=True)
    supplier_id = models.IntegerField(null=True, blank=True)
    supplier_financial_id = models.IntegerField(null=True, blank=True)
    demand_id = models.IntegerField(null=True, blank=True)
    invoice_no = models.IntegerField(null=True, blank=True)
    invoice_amount = models.FloatField(max_length=80, blank=False, null=False, default=Decimal(0.00))
    invoice_date = models.DateField(null=True, blank=True, default=datetime.now())
    due_date = models.DateField(null=True, blank=True, default=datetime.now())
    status_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

# Create Invoice table end.
