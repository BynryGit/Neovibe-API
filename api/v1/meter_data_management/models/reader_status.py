__author__ = "chinmay"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Schedule
# Description : It is Read Cycle table. This table will save all the read Cycles.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Chinmay Pathak
# Creation Date : 08/01/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from datetime import datetime # importing package for datetime
from v1.commonapp.models.meter_status import get_meter_status_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.contrib.postgres.fields import JSONField


# Create ReadCycle Table Start

class ReaderStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    meter_status_id = models.BigIntegerField(null=False, blank=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    status_code = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True)

    @property
    def get_meter_status(self):
        meter_status = get_meter_status_by_id(self.meter_status_id)
        return meter_status

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

# Create ReadCycle Table end


def get_reader_status_by_id(id):
    try:
        return ReaderStatus.objects.get(id=id, is_active=True)
    except:
        return False


def get_reader_status_by_id_string(id_string):
    try:
        return ReaderStatus.objects.get(id_string=id_string, is_active=True)
    except:
        return False