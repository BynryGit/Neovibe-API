# Table Header
# Table Type : Lookup (Local)
# Table Name : Upload Status
# Description :
# Frequency of data changes : Low
# Sample Table Data : "Accepted", "Rejected", "Send"
# Reference Table : Route Upload Status
# Author : Akshay
# Creation Date : 18-06-2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Route Upload Status table start

class RouteUploadStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Route Upload Status table end


def get_route_upload_status_by_id(id):
    try:
        return RouteUploadStatus.objects.get(id=id)
    except:
        return False


def get_route_upload_status_by_id_string(id_string):
    try:
        return RouteUploadStatus.objects.get(id_string=id_string)
    except:
        return False
