# Table Header
# module : S&M | sub - module : Survey and Campaign
# Table Type : Lookup (Global)
# Table Name : 2.12.25 Frequency
# Description : It is a global lookup table that stores frequencies(time period)
# Sample Table Data: 1 month, 2 month;
# Frequency of data changes : Low
# Reference Table : 2.3.8 Campaign Transaction Table, 2.4.6 Asset-SOP details,
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database

# Create Frequency table start
class Frequency(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
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
# Create Frequency table end

def get_frequency_by_tenant_id_string(tenant_id_string):
    return Frequency.objects.filter(tenant__id_string=tenant_id_string)

def get_frequency_by_id_string(id_string):
    return Frequency.objects.get(id_string = id_string)

def get_frequency_by_id(id):
    return Frequency.objects.get(id = id)
