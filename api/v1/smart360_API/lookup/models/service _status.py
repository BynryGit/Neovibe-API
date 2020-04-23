# table header
# module: Consumer Care & Ops | sub-module - Consumer, services
# table type: lookup
# table name: 2.12.48 Service Status (Local)
# table description: Lookup table for consumer services in Consumer care & ops
# frequency of data changes: low
# sample table data: "Received","Assigned", "Inprogress" "Completed","Rejected","Hold"
# reference tables: 2.2.1 Utility Services Master #todo: table name to be checked
# auther: Gauri Deshmukh
# creation date: 22/4/2020

#change history
#<ddmmyyyy>-<changes>-<auther>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


#Create ServiceStatus table start
class ServiceStatus(models.Model):
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

 # Create ServiceStatus table end