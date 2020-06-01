# Table header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name : 2.12.7 City
# Description : It is a global lookup table that stores cities within the countries with respect to tenants
# Frequency of data changes : Low
# Sample Table Data : "Pune", "Nagpur", "Bharatpur"
# Reference Table :
# Author : Saloni Monde
# Creation Date : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database

# Create Tenant City table start


class TenantCity(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    tenant_state_id = models.BigIntegerField(blank=True, null=True)
    tenant_country_id = models.BigIntegerField(null=True, blank=True)
    tenant_region_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Tenant City table end


def get_tenant_city_by_id_string(id_string):
    return TenantCity.objects.get(id_string = id_string)


def get_tenant_city_by_id(id):
    return TenantCity.objects.get(id = id)
