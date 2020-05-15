# Table Header
# Modules : Tenant, Utility | sub-modules : Tenant Master, Utility Master
# Table Type : Lookup (Global)
# Table Name :
# Description : A global lookup table that stores regions with respect to tenants.
# Frequency of data changes : Low
# Sample Table Data : "Americas", "Asia","Africa"
# Reference Table : 2.1 Utility Master
# Author : Saloni Monde
# Creation Date : 05-05-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database


# Create Tenant Region table start

class TenantRegion(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    region = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Tenant Region table end.
