# table header:
# module: Purchase | sub-module - Tender
# table type: lookup (local)
# table name: 2.12.89 Tender Status
# table description: A lookup table for the Tender status.
# frequency of data changes: low
# sample table data: "Initiated","Received","Approved","Rejected","Pending","Hold"
# reference tables:2.7.3 Tender Master
# Author: Gauri Deshmukh
# creation date: 22/4/2020

#change history
#<ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


#Create TenderStatus table start

class TenderStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

 # Create TenderStatus table end


def get_tender_status_by_id(id):
    try:
        return TenderStatus.objects.get(id=id)
    except:
        return False


def get_tender_status_by_id_string(id_string):
    try:
        return TenderStatus.objects.get(id_string=id_string)
    except:
        return False
