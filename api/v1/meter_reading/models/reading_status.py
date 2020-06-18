# Table Header
# Table Type : Lookup (Local)
# Table Name : 2.12.55 Reading Status
# Description : It Reading Status and ID of Reading Status  to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : "Validation one", "Validation two", "Complete"
# Reference Table : 2.3.8.4 Meter Reading
# Author : Jayshree Kumbhare
# Creation Date : 22-04-2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Reading Status table start

class ReadingStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.BigIntegerField(null=False, blank=False)
    updated_by = models.BigIntegerField(null=False, blank=False)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Reading Status table end


def get_reading_status_by_id(id):
    try:
        return ReadingStatus.objects.get(id=id)
    except:
        return False


def get_reading_status_by_id_string(id_string):
    try:
        return ReadingStatus.objects.get(id_string=id_string)
    except:
        return False
