__author__ = "chinmay"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Schedule
# Description : It is Read Cycle table. This table will save all the read Cycles.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Chinmay Pathak
# Creation Date : 08/01/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from datetime import datetime # importing package for datetime
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.zone import get_zone_by_id
from v1.commonapp.models.division import get_division_by_id
from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.contrib.postgres.fields import JSONField


# Create ReadCycle Table Start

class ReadCycle(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    city_id = models.BigIntegerField(null=False, blank=False)
    zone_id = models.BigIntegerField(null=False, blank=False)
    division_id = models.BigIntegerField(null=False, blank=False)
    area_id = models.BigIntegerField(null=False, blank=False)
    subarea_id = models.BigIntegerField(null=False, blank=False)
    route_json = JSONField(default='')
    label = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    @property
    def get_city(self):
        city = get_city_by_id(self.city_id)
        return city

    @property
    def get_zone(self):
        zone = get_zone_by_id(self.zone_id)
        return zone

    @property
    def get_division(self):
        division = get_division_by_id(self.division_id)
        return division

    @property
    def get_area(self):
        area = get_area_by_id(self.area_id)
        return area

    @property
    def get_subarea(self):
        subarea = get_sub_area_by_id(self.subarea_id)
        return subarea

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

# Create ReadCycle Table end


def get_read_cycle_by_id(id):
    try:
        return ReadCycle.objects.get(id=id, is_active=True)
    except:
        return False


def get_read_cycle_by_id_string(id_string):
    try:
        return ReadCycle.objects.get(id_string=id_string, is_active=True)
    except:
        return False


def get_all_read_cycles():
    return ReadCycle.objects.all(is_active=True)