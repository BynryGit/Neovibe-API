# table header
# module: Purchase
# table type : Master
# table name : 2.7.1 Request Master
# table description : This table will store all pending,approved,partial and rejected requests.
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

# Create Request Master table start

class RequestMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.IntegerField(null=True, blank=True)
    short_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    requester = models.IntegerField(null=True, blank=True)
    approver = models.IntegerField(null=True, blank=True)
    asset = models.IntegerField(null=True, blank=True)
    request_date = models.DateField(null=True, blank=True, default=datetime.now())
    request_due_date = models.DateField(null=True, blank=True, default=datetime.now())
    request_status = models.IntegerField(null=True, blank=True)
    country = models.IntegerField(null=True, blank=True)
    state = models.IntegerField(null=True, blank=True)
    city = models.IntegerField(null=True, blank=True)
    department = models.IntegerField(null=True, blank=True)
    project = models.IntegerField(null=True, blank=True)
    category = models.IntegerField(null=True, blank=True)
    sub_category = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.short_name

    def __unicode__(self):
        return self.short_name

# Create Request Master table end.
