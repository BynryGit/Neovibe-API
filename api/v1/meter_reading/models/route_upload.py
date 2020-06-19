# table header
# module: S&M, Consumer Care & Ops | sub-module - Meter Reading
# table type: lookup (local)
# table name: Route Upload
# table description:
# frequency of data changes: Medium
# sample table data:
# reference tables:
# Author: Akshay
# creation date: 18/06/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.meter_reading.models.bill_cycle import get_bill_cycle_by_id
from v1.meter_reading.models.route import get_route_by_id
from v1.meter_reading.models.route_upload_status import get_route_upload_status_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database

# Create Route Upload table start


class RouteUpload(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    token = models.CharField(max_length=200, null=False, blank=False)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    month = models.CharField(max_length=20, null=False, blank=False)
    upload_date = models.DateTimeField(null=True, blank=True)
    route_upload_status_id = models.BigIntegerField(null=True, blank=True) # send, accept, reject
    remark = models.CharField(max_length=500, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.token

    def __unicode__(self):
        return self.token

    @property
    def get_bill_cycle(self):
        bill_cycle = get_bill_cycle_by_id(self.bill_cycle_id)
        return bill_cycle

    @property
    def get_route(self):
        route = get_route_by_id(self.route_id)
        return route

    @property
    def get_route_upload_status(self):
        route_upload_status = get_route_upload_status_by_id(self.route_upload_status_id)
        return route_upload_status

# Create Route Upload table end


def get_route_upload_by_id(id):
    try:
        return RouteUpload.object.get(id=id)
    except:
        return False


def get_route_upload_by_id_string(id_string):
    try:
        return RouteUpload.object.get(id_string=id_string)
    except:
        return False
