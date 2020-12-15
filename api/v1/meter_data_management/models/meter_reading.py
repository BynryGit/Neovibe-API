# Table Header
# Module: Consumer Care and Ops | Sub-Module : Meter Reading
# Table Type : Master (Global)
# Table Name : 2.3.8.4 Meter Reading
# Description : When meter reader takes the reading and upload on server, entry will be created in meter reading table.
# Frequency of data changes : High
# Sample table : "Meter reading records consumer wise"
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime

from api.constants import get_file_name, METER_PICTURE
from v1.meter_data_management.models.bill_cycle import get_bill_cycle_by_id
from v1.meter_data_management.models.consumer import get_consumer_by_id
from v1.meter_data_management.models.jobcard import get_jobcard_by_id
from v1.meter_data_management.models.meter_image_type import get_meter_image_type_by_id
from v1.meter_data_management.models.meter_status import get_meter_status_by_id
from v1.meter_data_management.models.reader_status import get_reader_status_by_id
from v1.meter_data_management.models.reading_status import get_reading_status_by_id
from v1.meter_data_management.models.reading_taken_by import get_reading_taken_by_id
from v1.meter_data_management.models.route import get_route_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Meter Reading Table Start

def get_file_path(instance, filename):
    return get_file_name(METER_PICTURE, filename)


class MeterReading(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    reading_type_id = models.BigIntegerField(null=True, blank=True)
    reading_type_status_id = models.BigIntegerField(null=True, blank=True)
    month = models.CharField(max_length=200, null=True, blank=True)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    meter_no = models.CharField(max_length=200, null=True, blank=True)
    meter_image_type_id = models.BigIntegerField(null=True, blank=True)
    meter_image = models.FileField(upload_to=get_file_path, null=True, blank=True)
    jobcard_id = models.BigIntegerField(null=True, blank=True)
    current_reading = models.FloatField(null=True, blank=True)
    consumption = models.FloatField(null=True, blank=True)
    reading_date = models.DateTimeField(null=True, blank=True)
    reading_status_id = models.BigIntegerField(null=True, blank=True)
    meter_status_id = models.BigIntegerField(null=True, blank=True)
    reader_status_id = models.BigIntegerField(null=True, blank=True)
    reading_img = models.BigIntegerField(null=True, blank=True)
    reading_taken_by_id = models.BigIntegerField(null=True, blank=True)
    suspicious_activity = models.BooleanField(default=False)
    is_qr_tempered = models.BooleanField(default=False)
    is_solar_meter = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_assign_to_v1 = models.BooleanField(default=False)
    is_assign_to_v2 = models.BooleanField(default=False)
    is_account_verified = models.BooleanField(default=False)
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
    def get_jobcard(self):
        jobcard = get_jobcard_by_id(self.jobcard_id)
        return jobcard

    @property
    def get_reading_status(self):
        reading_status = get_reading_status_by_id(self.reading_status_id)
        return reading_status

    @property
    def get_meter_status(self):
        meter_status = get_meter_status_by_id(self.meter_status_id)
        return meter_status

    @property
    def get_reader_status_id(self):
        reader_status = get_reader_status_by_id(self.reader_status_id)
        return reader_status

    @property
    def get_reading_taken_by(self):
        reading_taken_by = get_reading_taken_by_id(self.reading_taken_by_id)
        return reading_taken_by

    @property
    def get_consumer(self):
        consumer = get_consumer_by_id(self.consumer_id)
        return consumer

    @property
    def get_meter_image_type(self):
        meter_image_type = get_meter_image_type_by_id(self.meter_image_type_id)
        return meter_image_type

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


def get_consumer_meter_reading_by_bill_month(consumer, month):
    try:
        return MeterReading.object.get(consumer_no=consumer, month=month)
    except:
        return False
