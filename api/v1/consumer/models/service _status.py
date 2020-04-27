# table header
# module: Consumer Care & Ops | sub-module - Consumer, services
# table type: lookup
# table name: 2.12.48 Service Status (Local)
# table description: Lookup table for consumer services in Consumer care & ops
# frequency of data changes: low
# sample table data: "Received","Assigned", "Inprogress" "Completed","Rejected","Hold"
# reference tables: 2.2.1 Utility Services Master #todo: table name to be checked
# Author: Gauri Deshmukh
# creation date: 22/4/2020

#change history
#<ddmmyyyy>-<changes>-<Author>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


#Create ServiceStatus table start
class ServiceStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    name = models.CharField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

 # Create ServiceStatus table end