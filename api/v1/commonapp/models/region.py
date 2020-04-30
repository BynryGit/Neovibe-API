# Table Header
# Modules : Tenant, Utility | sub-modules : Tenant Master, Utility Master
# Table Type : Lookup (Global)
# Table Name : 2.12.4 Region
# Description : A global lookup table that stores regions.
# Frequency of data changes : Low
# Sample Table Data : "Americas", "Asia","Africa"
# Reference Table : 2.1 Utility Master
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database

# Create Region table start

class Region(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=True, on_delete=models.SET_NULL) # to be removed
    utility = models.ForeignKey(UtilityMaster, blank=False, null=True, on_delete=models.SET_NULL) # to be removed
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Region table end.
