# table header
# module: Purchase
# table type : Master
# table name : 2.7.11 Receipt Table
# table description : This table will store all details of receipt according to store.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database
from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster

# Create Store Master table start

class Receipt(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    store_master_id = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    asset_code = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(null=True, blank=True)
    unit_price = models.CharField(max_length=200, blank=True, null=True)
    total_price = models.CharField(max_length=200, blank=True, null=True)
    tax = models.CharField(max_length=200, blank=True, null=True)
    gst = models.CharField(max_length=200, blank=True, null=True)
    bill_no = models.CharField(max_length=200, blank=True, null=True)
    bill_date = models.DateField(null=True, blank=True, default=datetime.now())
    description = models.CharField(max_length=500, blank=True, null=True)
    handover_to = models.IntegerField(null=True, blank=True)
    handover_date = models.DateField(null=True, blank=True, default=datetime.now())
    category_id = models.IntegerField(null=True, blank=True)
    sub_category_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

# Create Receipt table end.
