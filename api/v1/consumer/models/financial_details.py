# table header
# module: Sourcing
# table type : Master
# table name : 2.5.2 Financial Details
# table description : Table saves the financial  details of any Supplier that exists in the system.
# frequency of data changes : High
# sample table data : "Supplier Financial Details"
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

# Create Financial Details table start

class FinancialDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    supplier = models.IntegerField(null=True, blank=True)
    account_name = models.CharField(max_length=200, blank=True, null=True)
    account_no = models.CharField(max_length=200, blank=True, null=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    branch_name = models.CharField(max_length=200, blank=True, null=True)
    ifsc_code = models.CharField(max_length=200, blank=True, null=True)
    gst_no = models.CharField(max_length=200, blank=True, null=True)
    pan_no = models.CharField(max_length=200, blank=True, null=True)
    vat_no = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.supplier

    def __unicode__(self):
        return self.supplier

# Create Financial Details table end.




