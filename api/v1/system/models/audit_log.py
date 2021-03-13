# table header
# module: System
# table type : Master
# table name : 2.11.6. System - Audit Log
# table description : It is System table. It will contain details Audit log at system level
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
from django.utils import timezone # importing package for datetime


# Create Audit Log  table start

class AuditLog(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    action_time = models.DateTimeField(null=True, blank=True, default=timezone.now)
    module = models.BigIntegerField(null=True, blank=True)
    sub_module = models.BigIntegerField(null=True, blank=True)
    event = models.BigIntegerField(null=True, blank=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    sub_system = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id
# Create Audit Log end
