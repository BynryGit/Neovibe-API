__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Upload Route
# Description : It is upload Route table. This table will save all the upload route details.
# Frequency of data changes : Low
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 24/03/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route import get_route_by_id
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

# Create Upload Route Table Start


class UploadRoute(models.Model):
    UPLOAD_STATUS = (
        (0, 'NOT-SENT'),
        (1, 'SENT'),
        (2, 'RECEIVED'),
        (3, 'ACCEPTED'),
        (4, 'REJECTED'),
        (5, 'FAILED'),
    )

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    schedule_log_id = models.BigIntegerField(null=True, blank=True)
    read_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=False, blank=False)
    state = models.IntegerField(choices=UPLOAD_STATUS, default=0)
    upload_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    @property
    def get_read_cycle_name(self):
        read_cycle = get_read_cycle_by_id(self.read_cycle_id)
        return read_cycle

    @property
    def get_route_name(self):
        route = get_route_by_id(self.route_id)
        return route

    @property
    def get_schedule_log(self):
        schedule_log = get_schedule_log_by_id(self.schedule_log_id)
        return schedule_log

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return str(self.id_string)

# Create Upload Route Table end


def get_upload_route_by_id(id):
    try:
        return UploadRoute.objects.get(id=id, is_active=True)
    except:
        return False


def get_upload_route_by_id_string(id_string):
    try:
        return UploadRoute.objects.get(id_string=id_string, is_active=True)
    except:
        return False
