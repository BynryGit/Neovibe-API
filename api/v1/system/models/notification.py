# table header
# module: System
# table type : Master
# table name : 2.11.1. System - Notification
# table description : It is System table. It will contain details Notification generated at system level.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 27/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime
from django.db import models  # importing package for database
from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster


# Create Notification table start

class Notification(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    module = models.IntegerField(null=True, blank=True)
    submodule = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    frequency = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True, default=datetime.now())
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    action = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

# Create Notification table end.
