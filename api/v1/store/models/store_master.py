# table header
# module: Purchase
# table type : Master
# table name : 2.7.10 Store Master
# table description : This table will store all details of assets and spare material.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Store Master table start

class StoreMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    make = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    image = models.UrlField(null=False, blank=False)
    quantity = models.IntegerField(null=True, blank=True)
    manufacturing_year = models.CharField(max_length=200, blank=True, null=True)
    arrival_date = models.DateField(null=True, blank=True, default=datetime.now())
    amount = models.IntegerField(null=True, blank=True)
    contract = models.IntegerField(null=True, blank=True)
    vendor = models.IntegerField(null=True, blank=True)
    store_location = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id

# Create Store Master table end.
