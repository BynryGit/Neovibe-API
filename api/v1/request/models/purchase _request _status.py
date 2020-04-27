# table header:
# module: Purchase | sub-module - Requests
# table type: lookup (local)
# table name: 2.12.88 Purchase Request Status (Local)
# table description: A lookup table for status of purchase requests
# frequency of data changes: low
# sample table data: "Initiated","Received","Inprogress", "Partial","Completed""Rejected","Pending","Hold"
# reference tables: 2.7.1 Request Master
# Author: Gauri Deshmukh
# creation date: 22/4/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create PurchaseRequestStatus table start

class PurchaseRequestStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    status = models.CharField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

# Create PurchaseRequestStatus table end
