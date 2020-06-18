# Table Header
# Table Type : Lookup (Local)
# Table Name : 2.12.73 Service Type
# Description : Service type and ID of Service type to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : Installation, Conversion, Repair, Maintenance, Outage, Emergency, Meter Reading.
# Reference Table : 2.6.2 SOP Master
# Author : Jayshree Kumbhare
# Creation Date : 22/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Service Type table start

class ServiceType(models.Model):
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

# Create Service Type table end


def get_service_type_by_id_string(id_string):
    try:
        return ServiceType.objects.get(id_string=id_string)
    except:
        return False


def get_service_type_by_id(id):
    return ServiceType.objects.filter(id=id).last()


def get_service_type_by_name(name):
    try:
        return ServiceType.objects.get(name=name)
    except:
        return False
# End the Code
