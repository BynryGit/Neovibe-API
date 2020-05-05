# Table Header
# module: Consumer Care & Ops | sub-module - Consumer, Registration, Billing, Payments, Services, Complaints
# Table Type : Lookup (Global)
# Table Name :
# Description : It is a global lookup table that stores the currencies with respect to the tenants
# Frequency of data changes : Low
# Sample Table Data : "Rupee", "Pound", "Dollar"
# Reference Table :
# Author : Saloni Monde
# Creation Date : 05-05-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime

from django.db import models  # importing package for database

from v1.tenant.models.tenant_master import TenantMaster


# Create Tenant Currency table start

class TenantCurrency(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    currency = models.BigIntegerField(blank=False, null=False)
    tenant_country = models.BigIntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.currency

    def __unicode__(self):
        return self.currency

# Create Tenant Currency table end
