# Table Header
# Module: Consumer Care and Ops
# Table Type : Master
# Table Name : 2.4.1. Consumer Master
# Description :All active and inactive consumer for given tenant will be saved in this table all master values
# Frequency of data changes : High
# Sample table : Consumer 1, Consumer 2, Consumer 3, Consumer 4
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

import uuid
from datetime import datetime
import fsm
from rest_framework import status
from api.constants import *
from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.premises import get_premise_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models
from django.utils import timezone # importing package for datetime

# *********** CONSUMER CONSTANTS **************
CONSUMER_DICT = {
    "CREATED": 0,
    "APPROVED": 1,
    "INSTALLED": 2,
    "CONNECTED": 3,
    "TEMPORARY DISCONNECTED": 4,
    "PERMANENTLY DISCONNECTED": 5,
    "ARCHIVED": 6,
}


# Create Consumer Master table start.
class ConsumerMaster(models.Model, fsm.FiniteStateMachineMixin):
    CHOICES = (
        (0, 'CREATED'),
        (1, 'APPROVED'),
        (2, 'INSTALLED'),
        (3, 'CONNECTED'),
        (4, 'TEMPORARY DISCONNECTED'),
        (5, 'PERMANENTLY DISCONNECTED'),
        (6, 'ARCHIVED'),
    )

    ACCOUNT_TYPE = (
        (0, 'MASTER'),
        (1, 'CHILD'),
        (2, 'TEST'),
    )

    state_machine = {
        CONSUMER_DICT['CREATED']: (CONSUMER_DICT['APPROVED'], CONSUMER_DICT['CREATED'],),
        CONSUMER_DICT['APPROVED']: (CONSUMER_DICT['INSTALLED'],),
        CONSUMER_DICT['INSTALLED']: (CONSUMER_DICT['CONNECTED'],),
        CONSUMER_DICT['CONNECTED']: (
            CONSUMER_DICT['TEMPORARY DISCONNECTED'], CONSUMER_DICT['PERMANENTLY DISCONNECTED']),
        CONSUMER_DICT['TEMPORARY DISCONNECTED']: (CONSUMER_DICT['CONNECTED'],),
        CONSUMER_DICT['PERMANENTLY DISCONNECTED']: (CONSUMER_DICT['ARCHIVED'],),
        CONSUMER_DICT['ARCHIVED']: (CONSUMER_DICT['ARCHIVED'],),
    }

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    state = models.BigIntegerField(choices=CHOICES, default=0)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    master_consumer_no = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    phone_landline = models.CharField(max_length=200, null=True, blank=True)
    billing_address_line_1 = models.CharField(max_length=200, blank=True, null=True)
    billing_street = models.CharField(max_length=200, blank=True, null=True)
    billing_zipcode = models.CharField(max_length=200, null=True, blank=True)
    billing_state_id = models.BigIntegerField(null=True, blank=True)
    billing_city_id = models.BigIntegerField(null=True, blank=True)
    billing_area_id = models.BigIntegerField(null=True, blank=True)
    billing_sub_area_id = models.BigIntegerField(null=True, blank=True)
    registration_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    credit_rating_id = models.BigIntegerField(null=True, blank=True)
    account_type = models.BigIntegerField(choices=ACCOUNT_TYPE, null=True, blank=True)
    is_auto_pay = models.BooleanField(default=False)
    is_loan = models.BooleanField(default=False)
    is_upfront_amount = models.BooleanField(default=False)
    ownership_id = models.BigIntegerField(null=True, blank=True)
    is_address_same = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.phone_mobile + " " + str(self.id_string)

    def __unicode__(self):
        return self.phone_mobile

    @property
    def get_area(self):
        area = get_area_by_id(self.billing_area_id)
        return {
            'name': area.name,
            'id_string': area.id_string
        }

    @property
    def get_sub_area(self):
        sub_area = get_sub_area_by_id(self.billing_sub_area_id)
        return {
            'name': sub_area.name,
            'id_string': sub_area.id_string
        }

    @property
    def get_state(self):
        state = get_state_by_id(self.billing_state_id)
        return {
            'name': state.name,
            'id_string': state.id_string
        }

    @property
    def get_city(self):
        city = get_city_by_id(self.billing_city_id)
        return {
            'name': city.name,
            'id_string': city.id_string
        }

    @property
    def get_premise(self):
        premise = get_premise_by_id(self.premise_id)
        return {
            'name': premise.name,
            'id_string': premise.id_string
        }

    # Function for finite state machine state change
    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            self.save()
        except Exception as e:
            raise CustomAPIException("Consumer transition failed", status_code=status.HTTP_412_PRECONDITION_FAILED)


def get_consumer_by_id_string(id_string):
    try:
        return ConsumerMaster.objects.get(id_string=id_string)
    except Exception as e:
        return False


def get_consumer_by_id(id):
    try:
        return ConsumerMaster.objects.get(id=id)
    except:
        return False


def get_consumer_by_consumer_no(consumer_no):
    try:
        return ConsumerMaster.objects.get(consumer_no=consumer_no)
    except:
        return False


def get_consumer_by_registration_id(id):
    try:
        return ConsumerMaster.objects.get(registration_id=id)
    except:
        return False


def get_consumers_by_cycle_id(id):
    try:
        return ConsumerMaster.objects.filter(cycle_id=id)
    except:
        return False
