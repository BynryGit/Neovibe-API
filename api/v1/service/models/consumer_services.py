# Table Header
# Module: Consumer Care & Ops | Sub-Module : Consumer Services
# Table Type : Master (Global)
# Table Name : 2.4.4. Service Details
# Description : It is Service table. It will contain all service details like.Utility id,service status ,etc.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

import fsm
from rest_framework import status

from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

from django.db import models  # importing package for database

# *********** COMPLAINT CONSTANTS **************
SERVICE_DICT = {
    "CREATED"         : 0,
    "ACCEPTED"        : 1,
    "REJECTED"        : 2,
    "IN PROGRESS"     : 3,
    "NOT ASSIGNED"    : 4,
    "ASSIGNED"        : 5,
    "COMPLETED"       : 6,
    "HOLD"            : 7,
    "CLOSED"          : 8,
    "FAILED"          : 9,
    "ARCHIVED"        : 10,
}
# Create Service Details Table Start.

class ServiceDetails(models.Model, fsm.FiniteStateMachineMixin):
    CHOICES = (
        (0, 'CREATED'),
        (1, 'ACCEPTED'),
        (2, 'REJECTED'),
        (3, 'IN PROGRESS'),
        (4, 'NOT ASSIGNED'),
        (5, 'ASSIGNED'),
        (6, 'COMPLETED'),
        (7, 'HOLD'),
        (8, 'CLOSED'),
        (9, 'FAILED'),
        (10, 'ARCHIVED'),
    )

    state_machine = {
        SERVICE_DICT['CREATED']     : (SERVICE_DICT['NOT ASSIGNED'],),
        SERVICE_DICT['ACCEPTED']    : (SERVICE_DICT['COMPLETED'],),
        SERVICE_DICT['REJECTED']    : (SERVICE_DICT['ASSIGNED'],),
        SERVICE_DICT['IN PROGRESS'] : (SERVICE_DICT['REJECTED'], SERVICE_DICT['HOLD'],),
        SERVICE_DICT['NOT ASSIGNED']: (SERVICE_DICT['FAILED'], SERVICE_DICT['IN PROGRESS'], SERVICE_DICT['ASSIGNED']),
        SERVICE_DICT['ASSIGNED']    : (SERVICE_DICT['ACCEPTED'], SERVICE_DICT['REJECTED'],),
        SERVICE_DICT['COMPLETED']   : (SERVICE_DICT['HOLD'], SERVICE_DICT['CLOSED'],),
        SERVICE_DICT['HOLD']        : (SERVICE_DICT['ASSIGNED'], SERVICE_DICT['CLOSED']),
        SERVICE_DICT['CLOSED']      : (SERVICE_DICT['ARCHIVED'],),
        SERVICE_DICT['ARCHIVED']    : (SERVICE_DICT['ARCHIVED'],),
    }
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_request_no = models.CharField(max_length=200, null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    service_request_id = models.BigIntegerField(null=True, blank=True)
    service_type_id = models.BigIntegerField(null=True, blank=True)
    service_sub_type_id = models.BigIntegerField(null=True, blank=True)
    consumer_remark = models.CharField(max_length=500, null=True, blank=True)
    admin_remark = models.CharField(max_length=500, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    request_due_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    request_channel_id = models.BigIntegerField(null=True, blank=True)
    is_field_appointment = models.BooleanField(default=False)
    state = models.BigIntegerField(max_length=30, choices=CHOICES, default=0)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            self.save()
        except Exception as e:
            raise CustomAPIException("Service transition failed", status_code=status.HTTP_412_PRECONDITION_FAILED)

# Create Service Details table end.


def get_consumer_services_by_consumer_no(consumer_no):
    try:
        return ServiceDetails.objects.filter(consumer_no = consumer_no)
    except:
        return False


def get_consumer_service_by_id_string(id_string):
    try:
        return ServiceDetails.objects.get(id_string = id_string)
    except:
        return False


def get_consumer_service_by_id(id):
    try:
        return ServiceDetails.objects.get(id = id)
    except:
        return False