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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Sub Area table start

class SubArea(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    area = models.IntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# Create Sub Area table end

def get_sub_areas_by_tenant_id_string(id_string):
    return SubArea.objects.filter(tenant__id_string=id_string)

def get_sub_area_by_id_string(id_string):
    return SubArea.objects.get(id_string = id_string)

def get_sub_area_by_id(id):
    return SubArea.objects.get(id = id)