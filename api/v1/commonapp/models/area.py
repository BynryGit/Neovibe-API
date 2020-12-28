# table header
# module: All | sub-module - All
# Table Type : Lookup (Global)
# Table Name : 2.12.8 Area
# Description : It is a global lookup table that stores areas within cities
# Frequency of data changes : Low
# Sample table : "Shivajinagar", "Kothrod".
# Reference Table : 2.3.1 Survey Table, 2.3.4 Survey Consumer Table, 2.3.8 Campaign Transaction Table,
#                   2.3.2. Consumer - Registration, Service Assignment, Service AppoBigIntegerFieldment, 2.7.1. Employee
# Author : Jayshree Kumbhare
# Creation Date : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database

from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.views.custom_exception import ObjectNotFoundException
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.models.region import get_region_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.zone import get_zone_by_id


# Create Area table start


class Area(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    zone_id = models.BigIntegerField(blank=True, null=True)
    pin_code = models.CharField(max_length=200, blank=True, null=True)
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
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    @property
    def get_zone(self):
        zone = get_zone_by_id(self.zone_id)
        return zone


# Create Area table end

def get_areas_by_tenant_id_string(id_string):
    return Area.objects.filter(tenant__id_string=id_string)


def get_areas_by_utility_id_string(id_string):
    return Area.objects.filter(utility__id_string=id_string)


def get_area_by_id(id):
    try:
        uecyb=Area.objects.get(id=id)
        print("Hello:",uecyb)
        return Area.objects.get(id=id)
    except:
        return False


def get_area_by_id_string(id_string):
    try:
        return Area.objects.get(id_string=id_string)
    except:
        return False
