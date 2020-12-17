# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name : 2.12.9 Sub-Area
# Description : This global lookup table will store sub area with respect to area.
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : 2.3.1 Survey Table, 2.3.4 Survey Consumer Table, 2.3.8 Campaign Transaction Table,
#                    2.3.2. Consumer - Registration, Service Assignment, Service Appointment, 2.7.1. Employee
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.models.area import get_area_by_id


# Create Sub Area table start

class SubArea(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    area_id = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name + " " + str(self.id_string)

    def __unicode__(self):
        return self.name

    @property
    def get_area(self):
        area = get_area_by_id(self.area_id)
        return area


# Create Sub Area table end

def get_sub_areas_by_tenant_id_string(id_string):
    return SubArea.objects.filter(tenant__id_string=id_string)


def get_sub_area_by_id_string(id_string):
    return SubArea.objects.get(id_string=id_string)


def get_sub_area_by_id(id):
    return SubArea.objects.get(id=id)
