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
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models


# *********** CONSUMER CONSTANTS **************
CONSUMER_DICT = {
    "CREATED"                   : 0,
    "REGISTERED"                : 1,
    "INSTALLED"                 : 2,
    "CONNECTED"                 : 3,
    "TEMPORARY DISCONNECTED"    : 4,
    "PERMANENTLY DISCONNECTED"  : 5,
    "ARCHIVED"                  : 6,
}

# Create Consumer Master table start.
class ConsumerMaster(models.Model, fsm.FiniteStateMachineMixin):
    CHOICES = (
        (0, 'CREATED'),
        (1, 'REGISTERED'),
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
        CONSUMER_DICT['CREATED']                    : (CONSUMER_DICT['REGISTERED'],CONSUMER_DICT['CREATED'],),
        CONSUMER_DICT['REGISTERED']                 : (CONSUMER_DICT['INSTALLED'],),
        CONSUMER_DICT['INSTALLED']                  : (CONSUMER_DICT['CONNECTED'],),
        CONSUMER_DICT['CONNECTED']                  : (CONSUMER_DICT['TEMPORARY DISCONNECTED'], CONSUMER_DICT['PERMANENTLY DISCONNECTED']),
        CONSUMER_DICT['TEMPORARY DISCONNECTED']     : (CONSUMER_DICT['CONNECTED'],),
        CONSUMER_DICT['PERMANENTLY DISCONNECTED']   : (CONSUMER_DICT['ARCHIVED'],),
        CONSUMER_DICT['ARCHIVED']                   : (CONSUMER_DICT['ARCHIVED'],),
    }

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    master_consumer_no = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    phone_landline = models.CharField(max_length=200, null=True, blank=True)
    address_line_1 = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
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
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.phone_mobile

    def __unicode__(self):
        return self.phone_mobile

    # Function for finite state machine state change
    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            self.save()
        except Exception as e:
            raise CustomAPIException("Consumer transition failed", status_code=status.HTTP_412_PRECONDITION_FAILED)


def get_consumer_by_id_string(id_string):
    try:
        return ConsumerMaster.objects.get(id_string = id_string)
    except Exception as e:
        return False


def get_consumer_by_id(id):
    try:
        return ConsumerMaster.objects.get(id = id)
    except:
        return False


def get_consumer_by_consumer_no(consumer_no):
    try:
        return ConsumerMaster.objects.get(consumer_no = consumer_no)
    except:
        return False


def get_consumer_by_registration_id(id):
    try:
        return ConsumerMaster.objects.get(registration_id = id)
    except:
        return False


def get_consumers_by_cycle_id(id):
    try:
        return ConsumerMaster.objects.filter(cycle_id = id)
    except:
        return False
