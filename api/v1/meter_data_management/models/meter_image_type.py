# Table Header : Meter Image Type
# Table Type : Lookup (Local)
# Table Name : 2.12.58 Meter Image Type
# Description : Meter Image Type and ID of Meter Image Type to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : 2.3.8.5 Meter Reading Images
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Meter Image Type Table Start

class MeterImageType(models.Model):
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

# Create Meter Image Type Table end


def get_meter_image_type_by_id(id):
    try:
        return MeterImageType.objects.get(id=id)
    except:
        return False


def get_meter_image_type_id_string(id_string):
    try:
        return MeterImageType.objects.get(id_string=id_string)
    except:
        return False
