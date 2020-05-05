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

from v1.tenant.models.tenant_master import TenantMaster


# Create Tenant Country table start

class Country(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    country = models.BigIntegerField(null=True, blank=True)
    tenant_region = models.BigIntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Tenant Country table end
