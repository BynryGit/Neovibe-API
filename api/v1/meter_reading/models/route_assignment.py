# table header
# module: S&M, Consumer Care & Ops | sub-module - Meter Reading
# table type: lookup (local)
# table name: Route Assignment
# table description: A lookup tables to be used for meter reading routes
# frequency of data changes: Medium
# sample table data:
# reference tables: 2.3.8.2 Reading Consumer Master, 2.3.8.3 Jobcard, 2.3.8.4 Meter Reading
# Author: Akshay
# creation date: 16/06/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from master.models import get_user_by_id
from v1.meter_reading.models.bill_cycle import get_bill_cycle_by_id
from v1.meter_reading.models.route import get_route_by_id
from v1.meter_reading.models.route_assignment_status import get_route_assignment_status_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database

# Create Route Details table start


class RouteAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    meter_reader_id = models.BigIntegerField(null=True, blank=True)
    assign_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    month = models.CharField(max_length=20, blank=False, null=False)
    status_id = models.BigIntegerField(null=True, default=1, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.route_id

    def __unicode__(self):
        return self.route_id

    @property
    def get_bill_cycle(self):
        bill_cycle = get_bill_cycle_by_id(self.bill_cycle_id)
        return bill_cycle

    @property
    def get_route(self):
        route = get_route_by_id(self.route_id)
        return route

    @property
    def get_meter_reader(self):
        meter_reader = get_user_by_id(self.meter_reader_id)
        return meter_reader

    @property
    def get_route_assignment_status(self):
        route_assignment_status = get_route_assignment_status_by_id(self.status_id)
        return route_assignment_status

# Create RouteDetails table end


def get_route_assignment_by_id(id):
    try:
        return RouteAssignment.object.get(id=id)
    except:
        return False


def get_route_assignment_by_id_string(id_string):
    try:
        return RouteAssignment.object.get(id_string=id_string)
    except:
        return False
