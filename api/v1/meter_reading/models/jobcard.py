# Table Header
# Module: Consumer Ops | Sub-Module : Meter Reading
# Table Type : Master (Global)
# Table Name : 2.3.8.3 Jobcard
# Description : Assigned and De-assigned record are created in this table consumer wise and month wise.
# Frequency of data changes : High
# Sample table : "Consumer Details monthly"
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from master.models import get_user_by_id
from v1.meter_reading.models.bill_cycle import get_bill_cycle_by_id
from v1.meter_reading.models.route import get_route_by_id
from v1.meter_reading.models.route_assignment import get_route_assignment_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Jobcard Table Start.

class Jobcard(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    meter_reader_id = models.BigIntegerField(null=True, blank=True)
    month = models.CharField(max_length=200, null=True, blank=True)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    route_assigned_id = models.BigIntegerField(null=True, blank=True)
    assign_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    status_id = models.BigIntegerField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    is_deleted_for_mr = models.BooleanField(default=False)
    is_reading_completed = models.BooleanField(default=False)
    is_revisit = models.BooleanField(default=False)
    is_meter_reading = models.BooleanField(default=False)
    is_bill_distribution = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

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
    def get_route_assignment(self):
        route_assigned = get_route_assignment_by_id(self.route_assigned_id)
        return route_assigned

# Create Jobcard Table End.


def get_jobcard_by_id(id):
    try:
        return Jobcard.objects.get(id=id)
    except:
        return False


def get_jobcard_by_id_string(id_string):
    try:
        return Jobcard.objects.get(id_string=id_string)
    except:
        return False
