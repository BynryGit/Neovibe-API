# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading
# Table Type : Master (Global)
# Table Name : 2.3.8.2 Temp Consumer Master
# Description : Data will be store month wise,whose reading should be taken for the specific month.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime

from v1.meter_reading.models.bill_cycle import get_bill_cycle_by_id
from v1.meter_reading.models.route import get_route_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Temp Consumer Master Table Start

class Consumer(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    address_line_1 = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.BigIntegerField(null=True, blank=True)
    country_id = models.BigIntegerField(null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    subarea_id = models.BigIntegerField(null=True, blank=True)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    bill_month = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    meter_no = models.CharField(max_length=200, null=True, blank=True)
    meter_status_id = models.BigIntegerField(null=True, blank=True)
    current_reading = models.CharField(max_length=200, null=True, blank=True)
    reading_date = models.DateTimeField(null=True, blank=True)
    reading_status_id = models.BigIntegerField(null=True, blank=True)
    reader_status_id = models.BigIntegerField(null=True, blank=True)
    reading_img = models.BigIntegerField(null=True, blank=True)
    scheme_id = models.BigIntegerField(null=True, blank=True)
    outstanding = models.BigIntegerField(null=True, blank=True)
    meter_reading_id = models.BigIntegerField(null=True, blank=True)
    jobcard_id = models.BigIntegerField(null=True, blank=True)
    month = models.CharField(max_length=200, null=True, blank=True)
    suspicious_activity = models.BooleanField(default=False)
    is_qr_tempered = models.BooleanField(default=False)
    reading_taken_by = models.BigIntegerField(null=True, blank=True)
    is_solar_meter = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_account_verified = models.BooleanField(default=False)
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

# Create Temp Consumer Master Table end


def get_consumer_by_id(id):
    try:
        return Consumer.objects.get(id=id)
    except:
        return False


def get_consumer_by_id_string(id_string):
    try:
        return Consumer.objects.get(id_string=id_string)
    except:
        return False