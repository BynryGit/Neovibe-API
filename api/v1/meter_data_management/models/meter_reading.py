__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module :
# Table Type : Master
# Table Name : Meter Reading
# Description : It is meter reading table. This table will save all the meter reading details.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 09/02/2021

from datetime import datetime # importing package for datetime
from api.constants import get_file_name, METER_PICTURE
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Meter Reading Table Start

def get_file_path(instance, filename):
    return get_file_name(METER_PICTURE, filename)


class MeterReading(models.Model):
    READING_STATUS = (
        (0, 'VALIDATION_1'),
        (1, 'VALIDATION_2'),
        (2, 'COMPLETED'),
        (3, 'REVISITE'),
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    read_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    activity_type_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    jobcard_id = models.BigIntegerField(null=True, blank=True)
    meter_status_id = models.BigIntegerField(null=True, blank=True)
    reader_status_id = models.BigIntegerField(null=True, blank=True)
    reading_taken_by_id = models.BigIntegerField(null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    meter_no = models.CharField(max_length=200, null=True, blank=True)
    meter_image = models.FileField(upload_to=get_file_path, null=True, blank=True)
    current_reading = models.CharField(max_length=200, null=True, blank=True)
    consumption = models.CharField(max_length=200, null=True, blank=True)
    reading_date = models.DateTimeField(null=True, blank=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    reading_status = models.IntegerField(choices=READING_STATUS, default=0)
    is_duplicate = models.BooleanField(default=False)
    is_assign_to_v1 = models.BooleanField(default=False)
    is_assign_to_v2 = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

# Create Meter Reading Table end


def get_meter_reading_by_id(id):
    try:
        return MeterReading.objects.get(id=id)
    except:
        return False


def get_meter_reading_by_id_string(id_string):
    try:
        return MeterReading.objects.get(id_string=id_string)
    except:
        return False
