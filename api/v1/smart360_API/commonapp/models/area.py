# table header
# module: All | sub-module - All
# Table Type : Lookup (Global)
# Table Name : 2.12.8 Area
# Description : It is a global lookup table that stores areas within cities
# Frequency of data changes : Low
# Sample table : "Shivajinagar", "Kothrod".
# Reference Table : 2.3.1 Survey Table, 2.3.4 Survey Consumer Table, 2.3.8 Campaign Transaction Table,
#                   2.3.2. Consumer - Registration, Service Assignment, Service AppoIntegerFieldment, 2.7.1. Employee
# Author : Jayshree Kumbhare
# Creation Date : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Area table start

class Area(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    city = models.IntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# Create Area table end

def get_areas_by_tenant_id_string(id_string):
    return Area.objects.filter(tenant__id_string=id_string)


def get_area_by_id(id):
    return Area.objects.get(id = id)


def get_area_by_id_string(id_string):
    return Area.objects.get(id_string=id_string)

