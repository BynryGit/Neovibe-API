__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Meter
# Description : It is meter table. This table will save all the meter details.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 15/02/2021


import uuid
import fsm
from rest_framework import status
from django.utils import timezone # importing package for datetime
from django.db import models
from api.constants import get_file_name, METER_PICTURE
from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.commonapp.models.meter_status import get_meter_status_by_id
from v1.commonapp.models.premises import get_premise_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id
from v1.meter_data_management.models.meter_make import get_meter_make_by_id
from v1.meter_data_management.models.route import get_route_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_product import get_utility_product_by_id
from v1.commonapp.views.custom_exception import CustomAPIException


def get_file_path(instance, filename):
    return get_file_name(METER_PICTURE, filename)


# *********** STATE CONSTANTS **************
STATE_DICT = {
    "NOT-ASSIGNED": 0,
    "ASSIGNED": 1,
}


class Meter(models.Model, fsm.FiniteStateMachineMixin):
    STATE = (
        (0, 'NOT-ASSIGNED'),
        (1, 'ASSIGNED'),
    )

    state_machine = {
        STATE_DICT['NOT-ASSIGNED']: (STATE_DICT['ASSIGNED'],),
        STATE_DICT['ASSIGNED']: (STATE_DICT['NOT-ASSIGNED'],),
    }

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    route_id = models.BigIntegerField(null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    category_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    meter_type_id = models.BigIntegerField(null=True, blank=True)
    smart_meter_source_id = models.BigIntegerField(null=True, blank=True)
    meter_make_id = models.BigIntegerField(null=True, blank=True)
    state = models.IntegerField(choices=STATE, default=0)
    meter_status = models.IntegerField(null=True, blank=True)
    reader_status = models.IntegerField(null=True, blank=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    meter_no = models.CharField(max_length=200, blank=False, null=False)
    device_no = models.CharField(max_length=200, blank=False, null=False)
    meter_digit = models.BigIntegerField(null=True, blank=True)
    meter_image = models.FileField(upload_to=get_file_path, null=True, blank=True)
    address_line_1 = models.CharField(max_length=200, blank=True, null=True)
    address_line_2 = models.CharField(max_length=200, blank=True, null=True)
    current_reading = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    install_date = models.DateTimeField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)

    @property
    def get_state_name(self):
        state = get_state_by_id(self.state_id)
        return state

    @property
    def get_city_name(self):
        city = get_city_by_id(self.city_id)
        return city

    @property
    def get_area_name(self):
        area = get_area_by_id(self.area_id)
        return area

    @property
    def get_sub_area_name(self):
        subarea = get_sub_area_by_id(self.sub_area_id)
        return subarea

    @property
    def get_route_name(self):
        route = get_route_by_id(self.route_id)
        return route

    @property
    def get_premise_type(self):
        premise = get_premise_by_id(self.premise_id)
        return premise

    @property
    def get_category_name(self):
        category = get_global_lookup_by_id(self.category_id)
        return category

    @property
    def get_meter_type_name(self):
        meter_type = get_global_lookup_by_id(self.meter_type_id)
        return meter_type

    @property
    def get_utility_product_name(self):
        utility_product_type = get_utility_product_by_id(self.utility_product_id)
        return utility_product_type

    @property
    def get_meter_make(self):
        meter_make = get_meter_make_by_id(self.meter_make_id)
        return meter_make

    @property
    def get_meter_status_name(self):
        meter_status = get_meter_status_by_id(self.meter_status)
        return meter_status

    def __str__(self):
        return self.meter_no

    def __unicode__(self):
        return self.meter_no

    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            self.save()
        except Exception as ex:
            raise CustomAPIException(STATE_DICT, status_code=status.HTTP_412_PRECONDITION_FAILED)


def get_meter_by_id(id):
    try:
        return Meter.objects.get(id=id, is_active=True)
    except:
        return None


def get_meter_by_id_string(id_string):
    try:
        return Meter.objects.get(id_string=id_string, is_active=True)
    except:
        return False

def get_meter_by_number(no):
    try:
        return Meter.objects.get(meter_no=no, is_active=True)
    except:
        return None
