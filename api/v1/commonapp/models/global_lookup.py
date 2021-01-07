__author__ = "aki"

# table header
# module: All
# Table Type : Lookup (Global)
# Table Name : Global Lookup
# Description : Used to save all lookup value
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : All
# Author : Akshay Nibrad
# Creation Date : 06/01/2021

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Read Cycle table start

class Global_Lookup(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    module = models.CharField(max_length=200, blank=False, null=False)
    sub_module = models.CharField(max_length=200, blank=False, null=False)
    category = models.CharField(max_length=200, blank=False, null=False)
    key = models.CharField(max_length=200, blank=False, null=False) # Always small case
    value = models.CharField(max_length=200, blank=False, null=False) # Camel case
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.category

    def __unicode__(self):
        return self.category

# Create Read Cycle table end


def get_global_lookup_by_id(id):
    try:
        return Global_Lookup.objects.get(id=id)
    except:
        return False


def get_global_lookup_by_id_string(id_string):
    try:
        return Global_Lookup.objects.get(id_string=id_string)
    except:
        return False
