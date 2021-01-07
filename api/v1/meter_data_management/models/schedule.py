__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Schedule
# Description : It is schedule table. This table will save all the schedules month wise and cycle wise.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 06/01/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from datetime import datetime # importing package for datetime
from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.commonapp.models.premises import get_premise_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id
from v1.commonapp.models.zone import get_zone_by_id
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


# Create Schedule Table Start

class Schedule(models.Model):
    SCHEDULE_STATUS = (
        (0, 'PENDING'),
        (1, 'COMPLETED'),
        (2, 'INPROGRESS'),
    )

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    city_id = models.BigIntegerField(null=False, blank=False)
    zone_id = models.BigIntegerField(null=True, blank=True)
    division_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
    premises_id = models.BigIntegerField(null=True, blank=True)
    read_cycle_id = models.BigIntegerField(null=True, blank=True)
    consumer_type_id = models.BigIntegerField(null=True, blank=True)
    schedule_type_id = models.BigIntegerField(null=True, blank=True)
    activity_type_id = models.BigIntegerField(null=False, blank=False)
    schedule_status = models.IntegerField(choices=SCHEDULE_STATUS, default=0)
    month = models.CharField(max_length=200, null=False, blank=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    @property
    def get_city_name(self):
        city = get_city_by_id(self.city_id)
        return city

    @property
    def get_zone_name(self):
        zone = get_zone_by_id(self.zone_id)
        return zone

    # @property
    # def get_division_name(self):
    #     division = get_division_by_id(self.division_id)
    #     return division

    @property
    def get_area_name(self):
        area = get_area_by_id(self.area_id)
        return area

    @property
    def get_sub_area_name(self):
        sub_area = get_sub_area_by_id(self.sub_area_id)
        return sub_area

    @property
    def get_premises_name(self):
        premises = get_premise_by_id(self.premises_id)
        return premises

    @property
    def get_read_cycle_name(self):
        read_cycle = get_read_cycle_by_id(self.read_cycle_id)
        return read_cycle

    @property
    def get_consumer_type_name(self):
        consumer_type = get_global_lookup_by_id(self.consumer_type_id)
        return consumer_type

    @property
    def get_schedule_type_id_name(self):
        schedule_type = get_global_lookup_by_id(self.schedule_type_id)
        return schedule_type

    @property
    def get_activity_type_id_name(self):
        activity_type = get_global_lookup_by_id(self.activity_type_id)
        return activity_type

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return str(self.id_string)

# Create Schedule Table end


def get_schedule_by_id(id):
    try:
        return Schedule.objects.get(id=id)
    except:
        return False


def get_schedule_by_id_string(id_string):
    try:
        return Schedule.objects.get(id_string=id_string)
    except:
        return False


def get_all_schedules():
    return Schedule.objects.all(is_active=True)