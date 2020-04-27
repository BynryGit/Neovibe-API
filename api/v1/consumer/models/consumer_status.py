# table header:
# Module: Consumer Care & Ops | Sub-Modules - Consumer, Metering, Billing
# table type: lookup
# table name: 2.12.45 Consumer Status (Local)
# table description: It is a lookup table that stores the status of the consumer to be used in various tables.
# frequency of data changes: low
# sample table data: "Connected", "Disconnected", "Temp disconnected", "Hold","Registered"
# reference tables: 2.4.1. Consumer Master
# Author: Gauri Deshmukh
# creation date: 22/4/2020

#change history
#<ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID

from django.db import models  # importing package for database


#Create ConsumerStatus table start
class ConsumerStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    status = models.CharField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

 # Create ConsumerStatus table end