__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading
# Table Type : Master
# Table Name : New Consumer Details
# Description : It is consumer table. This table will save all the consumer details.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 07/06/2021

import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from master.models import get_user_by_id
from v1.commonapp.models.meter_status import get_meter_status_by_id
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.reader_status import get_reader_status_by_id
from v1.meter_data_management.models.route import get_route_by_id
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_product import get_utility_product_by_id


# Create Temp New Consumer Master Table Start
class NewConsumerDetail(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    schedule_log_id = models.BigIntegerField(null=True, blank=True)
    read_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    meter_reader_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    activity_type_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=False, blank=False)
    meter_no = models.CharField(max_length=200, null=False, blank=False)
    current_meter_reading = models.CharField(max_length=200, null=True, blank=True)
    meter_status_id = models.BigIntegerField(null=True, blank=True)
    reader_status_id = models.BigIntegerField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    is_discard = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.meter_no + ' ' + str(self.id_string)

    def __unicode__(self):
        return self.meter_no + ' ' +str(self.id_string)

    @property
    def get_schedule_log_name(self):
        schedule_log = get_schedule_log_by_id(self.schedule_log_id)
        return schedule_log

    @property
    def get_read_cycle_name(self):
        read_cycle = get_read_cycle_by_id(self.read_cycle_id)
        return read_cycle

    @property
    def get_route_name(self):
        route = get_route_by_id(self.route_id)
        return route

    @property
    def get_utility_product_name(self):
        utility_product = get_utility_product_by_id(self.utility_product_id)
        return utility_product

    @property
    def get_meter_reader_name(self):
        meter_reader = get_user_by_id(self.meter_reader_id)
        return meter_reader

    @property
    def get_meter_status_name(self):
        meter_status = get_meter_status_by_id(self.meter_status_id)
        return meter_status

    @property
    def get_reader_status_name(self):
        reader_status = get_reader_status_by_id(self.reader_status_id)
        return reader_status

# Create Temp New Consumer Master Table end


def get_new_consumer_detail_by_id(id):
    try:
        return NewConsumerDetail.objects.get(id=id)
    except:
        return False


def get_new_consumer_detail_by_id_string(id_string):
    try:
        return NewConsumerDetail.objects.get(id_string=id_string)
    except:
        return False