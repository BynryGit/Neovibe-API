# Table Header
# Table Type : Lookup (Local)
# Table Name : 2.12.73 Service Sub Type
# Description : Service Sub Type and ID of Service Sub Type to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : Service Type
# Author : Priyanka Kachare
# Creation Date : 16/12/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from v1.commonapp.models.service_type import get_service_type_by_id


# Create Service Type table start

class ServiceSubTypes(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_type_id = models.BigIntegerField(null=False, blank=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    
    @property
    def service_type(self):
        service_type = get_service_type_by_id(self.service_type_id)
        return service_type

# Create Service Type table end


def get_service_sub_type_by_id_string(id_string):
    try:
        return ServiceSubTypes.objects.get(id_string=id_string)
    except:
        return False


def get_service_sub_type_by_id(id):
    return ServiceSubTypes.objects.filter(id=id).last()


def get_service_sub_type_by_name(name):
    try:
        return ServiceSubTypes.objects.get(name=name)
    except:
        return False
# End the Code
