# Table Header
# module: Consumer Care & Ops | sub-module - Consumer, Registration, Billing, Payments, Services, Complaints
# Table Type : Lookup (Global)
# Table Name : 2.12.22 Channel
# Description : It is a global lookup table that stores various channels
# Frequency of data changes : Low
# Sample Table Data:  "branch", "mobile"
# Reference Table : 2.5.10 Payment Table.
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from django.db import models  # importing package for database

# Create Channel table start
from v1.tenant.models.tenant_master import TenantMaster


class Channel(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    key = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

def get_channel_by_id_string(id_string):
    return Channel.objects.get(id_string = id_string)

def get_channel_by_id(id):
    return Channel.objects.filter(id = id)

# Create Channel table end

