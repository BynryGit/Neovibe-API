# table header:
# Module: Consumer Care & Ops | Sub-Modules - Consumer, Metering, Billing
# table type: lookup
# table name: 2.12.45 Consumer Status (Local)
# table description: It is a lookup table that stores the status of the consumer to be used in various tables.
# frequency of data changes: low
# sample table data: "Connected", "Disconnected", "Temp disconnected", "Hold"
# reference tables: 2.4.1. Consumer Master
# auther: Gauri Deshmukh
# creation date: 22/4/2020

#change history
#<ddmmyyyy>-<changes>-<auther>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


#Create ConsumerStatus table start
class ConsumerStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    status = models.CharField(null=False, blank=False)
    created_by = models.CharField(null=False, blank=False)
    updated_by = models.CharField(null=False, blank=False)
    created_date = models.DateTime(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTime(null=True, blank=True, default=datetime.now())
    is_active = models.Boolean(default=False)

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

 # Create ConsumerStatus table end