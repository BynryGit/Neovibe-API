# table header
# table type : Master
# table name : 1.3 Tenant bank details
# table description : It will contain details for Tenant bank like bank name, branch name,etc.
# frequency of data changes : Low
# sample tale data :"HDFC Bank","Sinhgad road", "Pune"
# reference tables : 1.1 Tenant Master
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Tenant Bank Details table start.

class TenantBankDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    bank_id = models.IntegerField(null=True, blank=True)
    bank_name = models.CharField(max_length=200, blank=False, null=False)
    branch_id = models.IntegerField(null=True, blank=True)
    branch_name  = models.CharField(max_length=200, blank=False, null=False)
    branch_city  = models.CharField(max_length=200, blank=False, null=False)
    account_number = models.CharField(max_length=200, blank=False, null=False)
    account_type = models.CharField(max_length=200, blank=False, null=False)
    account_name = models.CharField(max_length=300, blank=False, null=False)
    pan_no = models.CharField(max_length=100, blank=False, null=False)
    gst_no  = models.CharField(max_length=100, blank=False, null=False)
    tax_id_no = models.CharField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.bank_id

    def __unicode__(self):
        return self.bank_id

# Create Tenant Bank Details table end.
