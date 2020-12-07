# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name : 2.12.6 State
# Description : It is a global lookup table that stores the states with countries
# Frequency of data changes : Low
# Sample Table Data : Maharashtra, Assam, Bihar.
# Reference Table : 2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.7.1. Employee, 2.7.7. Branch details,
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.models.region import get_region_by_id
from v1.commonapp.models.country import get_country_by_id


# Create State table start


class State(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    country_id = models.BigIntegerField(blank=True, null=True)
    region_id = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_region(self):
        region = get_region_by_id(self.region_id)
        return region

    @property
    def get_country(self):
        country = get_country_by_id(self.country_id)
        return country


# Create State table end


def get_state_by_id_string(id_string):
    return State.objects.get(id_string=id_string)


def get_state_by_id(id):
    return State.objects.get(id=id)

# End the Code
