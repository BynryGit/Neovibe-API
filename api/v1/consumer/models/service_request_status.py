# Table Header
# Module : Consumer Care & Ops
# Table Type : Lookup (Local)
# Table Name : 2.12.74 Service Request Status
# Description : Service Request Status and ID of Service Request Status  to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : Unresolved, In Progress, Complete, Closed, Pending.
# Reference Table : 2.6.1 Service Request
# Author : Jayshree Kumbhare
# Creation Date : 22/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID

from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Service Request Status table start

class ServiceRequestStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.BigIntegerField(null=False, blank=False)
    updated_by = models.BigIntegerField(null=False, blank=False)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Service Request Status table end
