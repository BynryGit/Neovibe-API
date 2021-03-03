# table Header
# module: Purchase | sub-module - Store
# table type: lookup (local)
# table name: 2.12.90 Store Type
# table description: A lookup table for store type
# frequency of data changes: Medium
# sample table data:
# reference tables: 2.7.10 Store Master
# Author: Gauri Deskhmukh
# creation date: 22/4/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create StoreType table start

class StoreType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    test = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create StoreType table end

def get_store_type_by_id(id):
    try:
        return StoreType.objects.filter(id=id).last()
    except:
        return False

def get_store_type_by_id_string(id_string):
    try:
        return StoreType.objects.get(id_string=id_string)
    except:
        return False