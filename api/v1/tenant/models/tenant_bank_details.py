# table header
# module: Tenant | sub-module - Invoices, Payments
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
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Tenant Bank Details table start.

class TenantBankDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    bank_name = models.CharField(max_length=200, blank=False, null=False)
    branch_name  = models.CharField(max_length=200, blank=False, null=False)
    branch_city  = models.CharField(max_length=200, blank=False, null=False)
    account_number = models.CharField(max_length=200, blank=False, null=False)
    account_type = models.CharField(max_length=200, blank=False, null=False)
    account_name = models.CharField(max_length=200, blank=False, null=False)
    ifsc_no = models.CharField(max_length=200, blank=False, null=False)
    pan_no = models.CharField(max_length=200, blank=False, null=False)
    gst_no  = models.CharField(max_length=200, blank=False, null=False)
    tax_id_no = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.bank_id

    def __unicode__(self):
        return self.bank_id

# Create Tenant Bank Details table end.

def get_bank_by_tenant_id_string(id_string):
    return TenantBankDetails.objects.filter(tenant_id_string=id_string,is_active=True)

def get_bank_by_id_string(id_string):
    return TenantBankDetails.objects.filter(id_string=id_string).last()


def get_bank_by_id(id):
    return TenantBankDetails.objects.filter(id=id).last()