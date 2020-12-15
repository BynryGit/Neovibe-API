# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name :
# Description : A global lookup table that stores countries within the regions
# Frequency of data changes : Low
# Sample Table Data : India
# Reference Table :
# Author : Saloni Monde
# Creation Date : 05-05-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database

# Create Tenant Country table start


class TenantCountry(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    tenant_region_id = models.BigIntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Tenant Country table end


def get_tenant_country_by_id(id):
    try:
        return TenantCountry.objects.get(id=id)
    except:
        return False


def get_tenant_country_by_id_string(id_string):
    try:
        return TenantCountry.objects.get(id_string=id_string)
    except:
        return False