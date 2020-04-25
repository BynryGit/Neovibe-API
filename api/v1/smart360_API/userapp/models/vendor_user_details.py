# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.4. Vendors User Details
# table description : A master table that stores details of all vendor user in the system.
# frequency of data changes : Low
# sample tale data :
# reference tables : Vendor Details
# author : Saloni Monde
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Vendor User Details table start

class VendorDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    vendor = models.IntegerField(blank=False, null=False)
    user = models.IntegerField(blank=False, null=False)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    account_no = models.CharField(max_length=200, blank=True, null=True)
    ifsc_code = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=200, blank=True, null=True)
    email_id = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.vendor

    def __unicode__(self):
        return self.vendor

# Create Vendor User Details table end
