# table header
# module: User
# table type : Master
# table name : User bank details
# table description : It will contain details for user bank like bank name, branch name,etc.
# frequency of data changes : Low
# sample tale data :"HDFC Bank","Sinhgad road", "Pune"
# reference tables : 1.1 Tenant Master
# author : Arpita Badwaik
# created on : 13/05/2020


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Tenant Bank Details table start.

class UserBankDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
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
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.bank_id

    def __unicode__(self):
        return self.bank_id

# Create Tenant Bank Details table end.


def get_bank_by_tenant_id_string(id_string):
    return UserBankDetails.objects.filter(tenant__id_string=id_string,is_active=True)


def get_bank_by_utility_id_string(id_string):
    return UserBankDetails.objects.filter(utility__id_string=id_string,is_active=True)


def get_bank_by_id_string(id_string):
    return UserBankDetails.objects.filter(id_string=id_string).last()


def get_bank_by_id(id):
    return UserBankDetails.objects.filter(id=id).last()
