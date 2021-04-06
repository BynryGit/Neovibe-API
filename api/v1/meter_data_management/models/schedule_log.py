__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Schedule Log
# Description : It is schedule log table. This table will save all the schedules log.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 08/01/2021


import fsm
import uuid  # importing package for GUID
from rest_framework import status
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from api.messages import SCHEDULE_LOG_TRANSITION
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.schedule import get_schedule_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_product import get_utility_product_by_id


# Create Schedule Table Start

# *********** SCHEDULE LOG CONSTANTS **************
SCHEDULE_LOG_STATUS_DICT = {
    "CREATED": 0,
    "NO-DATA": 1,
    "IN-PROGRESS": 2,
    "PARTIAL": 3,
    "COMPLETED": 4,
    "ARCHIVED": 5,
}


class ScheduleLog(models.Model, fsm.FiniteStateMachineMixin):
    SCHEDULE_LOG_STATUS = (
        (0, 'CREATED'),
        (1, 'NO-DATA'),
        (2, 'IN-PROGRESS'),
        (3, 'PARTIAL'),
        (4, 'COMPLETED'),
        (5, 'ARCHIVED'),
    )
    state_machine = {
        SCHEDULE_LOG_STATUS_DICT['CREATED']: (SCHEDULE_LOG_STATUS_DICT['IN-PROGRESS'],),
        SCHEDULE_LOG_STATUS_DICT['IN-PROGRESS']: (SCHEDULE_LOG_STATUS_DICT['NO-DATA'],
                                                  SCHEDULE_LOG_STATUS_DICT['PARTIAL'],
                                                  SCHEDULE_LOG_STATUS_DICT['COMPLETED'],),
        SCHEDULE_LOG_STATUS_DICT['NO-DATA']: (SCHEDULE_LOG_STATUS_DICT['PARTIAL'],
                                              SCHEDULE_LOG_STATUS_DICT['COMPLETED'],),
        SCHEDULE_LOG_STATUS_DICT['PARTIAL']: (SCHEDULE_LOG_STATUS_DICT['COMPLETED'],),
        SCHEDULE_LOG_STATUS_DICT['COMPLETED']: (SCHEDULE_LOG_STATUS_DICT['ARCHIVED'],),
    }

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    schedule_id = models.BigIntegerField(null=False, blank=False)
    read_cycle_id = models.BigIntegerField(null=False, blank=False)
    activity_type_id = models.BigIntegerField(null=False, blank=False)
    recurring_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    state = models.IntegerField(choices=SCHEDULE_LOG_STATUS, default=0)
    date_and_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    @property
    def get_schedule_name(self):
        schedule = get_schedule_by_id(self.schedule_id)
        return schedule

    @property
    def get_read_cycle_name(self):
        read_cycle = get_read_cycle_by_id(self.read_cycle_id)
        return read_cycle

    @property
    def get_activity_type(self):
        activity_type = get_global_lookup_by_id(self.activity_type_id)
        return activity_type

    @property
    def get_recurring_name(self):
        recurring = get_global_lookup_by_id(self.recurring_id)
        return recurring

    @property
    def get_utility_product_name(self):
        utility_product_type = get_utility_product_by_id(self.utility_product_id)
        return utility_product_type

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return str(self.id_string)

    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            self.save()
        except Exception as ex:
            raise CustomAPIException(SCHEDULE_LOG_TRANSITION, status_code=status.HTTP_412_PRECONDITION_FAILED)

# Create Schedule Table end


def get_schedule_log_by_id(id):
    try:
        return ScheduleLog.objects.get(id=id, is_active=True)
    except:
        return False


def get_schedule_log_by_id_string(id_string):
    try:
        return ScheduleLog.objects.get(id_string=id_string, is_active=True)
    except:
        return False
