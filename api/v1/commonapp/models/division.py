# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name : 2.12.5 Division
# Description : A global lookup table that stores Divisions within the zones
# Frequency of data changes : Low
# Author : Chinmay Pathak
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from django.db import models  # importing package for database
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_region import get_utility_region_by_id
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status
from v1.commonapp.models.zone import get_zone_by_id
from django.utils import timezone # importing package for datetime

# Create Division table start


class Division(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    zone_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_zone(self):
        zone = get_zone_by_id(self.zone_id)
        return zone

# Create Division table end


def get_division_by_id_string(id_string):
    return Division.objects.get(id_string=id_string)


def get_division_by_id(id):
    return Division.objects.get(id=id)

# End the Code
