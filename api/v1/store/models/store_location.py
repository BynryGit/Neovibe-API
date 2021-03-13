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
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.area import get_area_by_id
from django.utils import timezone # importing package for datetime

# Create StoreLocation table start
class StoreLocation(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    store_id = models.BigIntegerField(null=True, blank=True)
    store_name = models.CharField(max_length=200, blank=False, null=False)
    store_address = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.BigIntegerField(null=True, blank=True)
    longitude = models.BigIntegerField(null=True, blank=True)
    contact_mobile = models.BigIntegerField(null=True, blank=True)
    contact_landstore  = models.BigIntegerField(null=True, blank=True)
    city_id  = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.store_name

    def __unicode__(self):
        return self.store_name

    @property
    def get_city(self):
        city = get_city_by_id(self.city_id)
        return city

    @property
    def get_area(self):
        area = get_area_by_id(self.area_id)
        return area

# Create StoreLocation table end

def get_store_location_by_id(id):
    try:
        return StoreLocation.objects.filter(id=id).last()
    except:
        return False

def get_store_location_by_id_string(id_string):
    try:
        return StoreLocation.objects.get(id_string=id_string)
    except:
        return False
