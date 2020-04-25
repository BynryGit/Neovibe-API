# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.3. Vendor Details
# table description : A master table that stores details of all vendors in the system.
# frequency of data changes : Low
# sample tale data : "vendor1", "vendor2"
# reference tables :
# author : Saloni Monde
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Vendor Details table start

class VendorDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=500, null=True, blank=True)
    bank = models.CharField(max_length=200, null=True, blank=True)
    account_no = models.CharField(max_length=200, null=True, blank=True)
    ifsc_code = models.CharField(max_length=200, null=True, blank=True)
    phone_no_1 = models.CharField(max_length=200, null=True, blank=True)
    phone_no_2 = models.CharField(max_length=200, null=True, blank=True)
    address_line_1 = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    country = models.IntegerField(null=True, blank=True)
    city = models.IntegerField(null=True, blank=True)
    form_factor = models.IntegerField(null=True, blank=True)
    po_contact_no = models.CharField(max_length=200, null=True, blank=True)
    validity_start_date = models.DateField(null=True, blank=True, default=datetime.now())
    validity_expiry_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Vendor Details table end
