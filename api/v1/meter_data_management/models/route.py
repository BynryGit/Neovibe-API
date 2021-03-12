__author__ = "chinmay"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Schedule
# Description : It is Route table. This table will save all the Routes.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Chinmay Pathak
# Creation Date : 08/01/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from django.contrib.postgres.fields import JSONField
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


# Create Route Table Start

class Route(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    label = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    premises_json = JSONField()
    filter_json = JSONField()
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return str(self.name) + ""+str(self.id_string)

    def __unicode__(self):
        return self.name

# Create Route Table end


def get_route_by_id(id):
    try:
        return Route.objects.get(id=id, is_active=True)
    except:
        return False


def get_route_by_id_string(id_string):
    try:
        return Route.objects.get(id_string=id_string, is_active=True)
    except:
        return False


def get_route_by_name(name):
    try:
        return Route.objects.get(name=name, is_active=True)
    except:
        return False


def get_all_routes():
    return Route.objects.all(is_active=True)