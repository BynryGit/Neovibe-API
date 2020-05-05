# Table Header
# module : Tenant
# Table Type : Lookup (Global)
# Table Name :
# Description : It is a global lookup table that stores the states with countries with respect to tenants
# Frequency of data changes : Low
# Sample Table Data : Maharashtra, Assam, Bihar.
# Reference Table :
# Author : Saloni Monde
# Creation Date : 05-05-2020

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database


# Create Tenant State table start

class TenantState(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    state = models.BigIntegerField(null=True, blank=True)
    tenant_country = models.BigIntegerField(blank=False, null=False)
    tenant_region = models.BigIntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Tenant State table end
