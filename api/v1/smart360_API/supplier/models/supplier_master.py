# table header
# module: Sourcing
# table type : Master
# table name : Supplier  Master
# table description : The Supplier Master table saves the basic details of any Supplier that exists.
# frequency of data changes : High
# sample table data : "Supplier 1", "Supplier 2"
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


# Create Supplier Master table start

class SupplierMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    country = models.IntegerField(null=True, blank=True)
    state = models.IntegerField(null=True, blank=True)
    city = models.IntegerField(null=True, blank=True)
    source = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    phone_no = models.CharField(max_length=200, blank=True, null=True)
    email_id = models.CharField(max_length=200, blank=True, null=True)
    address_line_1 = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    payment = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Supplier Master table end.
