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
# Creation Date : 27/02/2021

import uuid  # importing package for GUID
from django.utils import timezone # importing package for datetime
from django.db import models  # importing package for database
from api.constants import get_file_name, METER_PICTURE
from master.models import get_user_by_id
from v1.meter_data_management.models.consumer_detail import get_consumer_detail_by_id
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route import get_route_by_id
from v1.meter_data_management.models.route_task_assignment import get_route_task_assignment_by_id
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.contrib.postgres.fields import JSONField
from v1.utility.models.utility_product import get_utility_product_by_id

# Create Meter Reading Table Start


def get_file_path(instance, filename):
    return get_file_name(METER_PICTURE, filename)


class MeterReading(models.Model):
    READING_STATUS = (
        (0, 'VALIDATION-ONE'),
        (1, 'VALIDATION-TWO'),
        (2, 'COMPLETED'),
        (3, 'REVISIT'),
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_detail_id = models.BigIntegerField(null=True, blank=True)
    read_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    route_task_assignment_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    schedule_log_id = models.BigIntegerField(null=True, blank=True)
    meter_reader_id = models.BigIntegerField(null=True, blank=True)
    validator_one_id = models.BigIntegerField(null=True, blank=True)
    validator_two_id = models.BigIntegerField(null=True, blank=True)
    meter_status_id = models.BigIntegerField(null=True, blank=True)
    meter_status_v1_id = models.BigIntegerField(null=True, blank=True)
    meter_status_v2_id = models.BigIntegerField(null=True, blank=True)
    reader_status_id = models.BigIntegerField(null=True, blank=True)
    reader_status_v1_id = models.BigIntegerField(null=True, blank=True)
    reader_status_v2_id = models.BigIntegerField(null=True, blank=True)
    reading_status = models.IntegerField(choices=READING_STATUS, default=0)
    meter_image = models.FileField(upload_to=get_file_path, null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    meter_no = models.CharField(max_length=200, null=True, blank=True)
    current_meter_reading = models.CharField(max_length=200, null=True, blank=True)
    current_meter_reading_v1 = models.CharField(max_length=200, null=True, blank=True)
    current_meter_reading_v2 = models.CharField(max_length=200, null=True, blank=True)
    meter_reading_json = JSONField(null=True, blank=True)
    additional_parameter_json = JSONField(null=True, blank=True)
    spot_bill_json = JSONField(null=True, blank=True)
    is_assign_to_v1 = models.BooleanField(default=False)
    is_assign_to_v2 = models.BooleanField(default=False)
    is_meter_matching = models.BooleanField(default=False)
    is_reading_matching = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    is_spot_bill = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    @property
    def get_consumer_detail(self):
        consumer_detail = get_consumer_detail_by_id(self.consumer_detail_id)
        return consumer_detail

    @property
    def get_read_cycle_name(self):
        read_cycle = get_read_cycle_by_id(self.read_cycle_id)
        return read_cycle

    @property
    def get_route_name(self):
        route = get_route_by_id(self.route_id)
        return route

    @property
    def get_route_task_assignmnet(self):
        route_task_assignment = get_route_task_assignment_by_id(self.route_task_assignment_id)
        return route_task_assignment

    @property
    def get_schedule_log_name(self):
        schedule_log = get_schedule_log_by_id(self.schedule_log_id)
        return schedule_log

    @property
    def get_utility_product_name(self):
        utility_product = get_utility_product_by_id(self.utility_product_id)
        return utility_product

    @property
    def get_meter_reader_name(self):
        meter_reader = get_user_by_id(self.meter_reader_id)
        return meter_reader

    @property
    def get_validator_one_name(self):
        validator_one = get_user_by_id(self.validator_one_id)
        return validator_one

    @property
    def get_validator_two_name(self):
        validator_two = get_user_by_id(self.validator_two_id)
        return validator_two

    def __str__(self):
        return self.meter_no + ' ' + str(self.id_string)

    def __unicode__(self):
        return self.meter_no + ' ' +  str(self.id_string)

# Create Meter Reading Table end


def get_meter_reading_by_id(id):
    try:
        return MeterReading.objects.get(id=id, is_active=True)
    except:
        return False


def get_meter_reading_by_id_string(id_string):
    try:
        return MeterReading.objects.get(id_string=id_string, is_active=True)
    except:
        return False
