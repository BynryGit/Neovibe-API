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
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime

# Create Store Master table start

class Receipt(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    store_master_id = models.BigIntegerField(null=True, blank=True)
    type = models.BigIntegerField(null=True, blank=True)
    asset_code = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.BigIntegerField(null=True, blank=True)
    unit_price = models.CharField(max_length=200, blank=True, null=True)
    total_price = models.CharField(max_length=200, blank=True, null=True)
    tax = models.CharField(max_length=200, blank=True, null=True)
    gst = models.CharField(max_length=200, blank=True, null=True)
    bill_no = models.CharField(max_length=200, blank=True, null=True)
    bill_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    description = models.CharField(max_length=500, blank=True, null=True)
    handover_to = models.BigIntegerField(null=True, blank=True)
    handover_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    category_id = models.BigIntegerField(null=True, blank=True)
    sub_category_id = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.type

    def __unicode__(self):
        return self.type

# Create Receipt table end.
