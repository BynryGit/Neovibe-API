__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Consumer Deatils
# Description : It is consumer table. This table will save all the consumer details.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 09/02/2021

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Temp Consumer Master Table Start

class ConsumerDetail(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    country_id = models.BigIntegerField(null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    subarea_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    read_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    activity_type_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile_1 = models.CharField(max_length=50, null=True, blank=True)
    phone_mobile_2 = models.CharField(max_length=50, null=True, blank=True)
    address_line_1 = models.CharField(max_length=500, null=True, blank=True)
    address_line_2 = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=50, null=True, blank=True)
    meter_digit = models.CharField(max_length=50, null=True, blank=True)
    meter_no = models.CharField(max_length=50, null=True, blank=True)
    prev_meter_reading = models.CharField(max_length=200, null=True, blank=True)
    prev_meter_status_id = models.BigIntegerField(null=True, blank=True)
    prev_reader_status_id = models.BigIntegerField(null=True, blank=True)
    net_meter = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

# Create Temp Consumer Master Table end


def get_consumer_by_id(id):
    try:
        return ConsumerDetail.objects.get(id=id)
    except:
        return False


def get_consumer_by_id_string(id_string):
    try:
        return ConsumerDetail.objects.get(id_string=id_string)
    except:
        return False