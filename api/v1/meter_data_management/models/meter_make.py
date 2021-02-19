__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops
# Table Type : Master
# Table Name : Meter
# Description : It is meter make table. This table will save all the meter make details.
# Frequency of data changes : low
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 19/02/2021


import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class MeterMake(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


def get_meter_make_by_id(id):
    try:
        return MeterMake.objects.get(id=id, is_active=True)
    except:
        return False


def get_meter_make_by_id_string(id_string):
    try:
        return MeterMake.objects.get(id_string=id_string, is_active=True)
    except:
        return False
