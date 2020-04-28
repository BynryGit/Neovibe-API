# table Header:
# module: Purchase | sub-module - Store
# table type: lookup (Local)
# table name: 2.12.91 Store Location
# table description: Lookup table for all store locations
# frequency of data changes: Medium
# sample table data: Shivaji Nagar, Kothrud, Aundh
# reference tables: 2.7.10 Store Master
# Author: Gauri Deshmukh
# creation date: 22/4/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create StoreLocation table start
class StoreLocation(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    store_name = models.CharField(max_length=200, blank=True, null=True)
    store_address = models.CharField(max_length=500, blank=True, null=True)
    contact_mobile = models.IntegerField(null=True, blank=True)
    contact_landstore  = models.IntegerField(null=True, blank=True)
    city_id  = models.IntegerField(null=True, blank=True)
    area_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.store_name

    def __unicode__(self):
        return self.store_name

# Create StoreLocation table end
