# Table Header
# Module: Consumer Care & Ops | Sub-Module : Validation
# Table Type : Master (Global)
# Table Name : 2.3.8.7 Validation
# Description : After submitting meter readings by meter reader, v1 and v2 records will be created per reading.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime

from master.models import get_user_by_id
from v1.meter_data_management.models.bill_cycle import get_bill_cycle_by_id
from v1.meter_data_management.models.meter_reading import get_meter_reading_by_id
from v1.meter_data_management.models.route import get_route_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Validation Details Table Start

class Validation(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    meter_reading_id = models.BigIntegerField(null=True, blank=True)
    month = models.CharField(max_length=200, null=True, blank=True)
    validation_type_id = models.BigIntegerField(null=True, blank=True)
    validator_id = models.BigIntegerField(null=True, blank=True)
    validator_meter_status_id = models.BigIntegerField(null=True, blank=True)
    validator_reader_status_id = models.BigIntegerField(null=True, blank=True)
    validator_reading = models.CharField(max_length=200, null=True, blank=True)
    validator_comment = models.CharField(max_length=500, null=True, blank=True)
    assigned_to = models.CharField(max_length=500, null=True, blank=True)
    validator_image_remark = models.CharField(max_length=500, null=True, blank=True)
    validated_on = models.DateTimeField(null=True, blank=True)
    is_meter_matching = models.BooleanField(default=False)
    is_reading_matching = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

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
    def get_validator(self):
        validator = get_user_by_id(self.validator_id)
        return validator

    @property
    def get_meter_reading(self):
        meter_reading = get_meter_reading_by_id(self.meter_reading_id)
        return meter_reading

# Create Validation Details Table end


def get_validation_by_id(id):
    try:
        return Validation.objects.get(id=id)
    except:
        return False


def get_validation_by_id_string(id_string):
    try:
        return Validation.objects.get(id_string=id_string)
    except:
        return False

