# table header
# module: S&M, Consumer Care & Ops | sub-module - Meter Reading
# table type: lookup (local)
# table name: 2.12.50 Route Details
# table description: A lookup tables to be used for meter reading routes
# frequency of data changes: Medium
# sample table data:R1, R2, R3, R4
# reference tables: 2.3.8.2 Reading Consumer Master, 2.3.8.3 Jobcard, 2.3.8.4 Meter Reading, 2.3.9 Invoice/Bill
# Author: Gauri Deshmukh
# creation date: 22/4/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database

# Create Route Details table start


class Route(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=200, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    city = models.BigIntegerField(null=True, blank=True)
    area = models.BigIntegerField(null=True, blank=True)
    subarea = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

# Create RouteDetails table end


def get_route_by_id(id):
    try:
        return Route.object.get(id=id)
    except:
        return False


def get_route_by_id_string(id_string):
    try:
        return Route.object.get(id_string=id_string)
    except:
        return False
