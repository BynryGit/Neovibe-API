__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Route Task Assignment
# Description : It is route task assignment table. This table will save all the task/job details.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 27/02/2021


import fsm
import uuid  # importing package for GUID
from rest_framework import status
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from api.messages import ROUTE_TASK_ASSIGNMENT_TRANSITION
from master.models import get_user_by_id
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route import get_route_by_id
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.contrib.postgres.fields import JSONField
from v1.commonapp.views.custom_exception import CustomAPIException

# Create Schedule Table Start

# *********** ROUTE TASK ASSIGNMENT CONSTANTS **************
ROUTE_TASK_ASSIGNMENT_STATUS_DICT = {
    "NOT-DISPATCHED": 0,
    "IN-PROGRESS": 1,
    "STARTED": 2,
    "DISPATCHED": 3,
    "PARTIAL": 4,
    "ASSIGN-FAIL": 5,
    "DE-ASSIGN-FAIL": 6,
    "COMPLETED": 7,
    "ARCHIVED": 8,
}


# Create Schedule Table Start

class RouteTaskAssignment(models.Model, fsm.FiniteStateMachineMixin):
    ROUTE_TASK_ASSIGNMENT_STATUS = (
        (0, 'NOT-DISPATCHED'),
        (1, 'IN-PROGRESS'),
        (2, 'STARTED'),
        (3, 'DISPATCHED'),
        (4, 'PARTIAL'),
        (5, 'ASSIGN-FAIL'),
        (6, 'DE-ASSIGN-FAIL'),
        (7, 'COMPLETED'),
        (8, 'ARCHIVED'),
    )
    state_machine = {
        ROUTE_TASK_ASSIGNMENT_STATUS_DICT['NOT-DISPATCHED']: (ROUTE_TASK_ASSIGNMENT_STATUS_DICT['IN-PROGRESS'],),
        ROUTE_TASK_ASSIGNMENT_STATUS_DICT['PARTIAL']: (ROUTE_TASK_ASSIGNMENT_STATUS_DICT['IN-PROGRESS'],),
        ROUTE_TASK_ASSIGNMENT_STATUS_DICT['ASSIGN-FAIL']: (ROUTE_TASK_ASSIGNMENT_STATUS_DICT['IN-PROGRESS'],),
        ROUTE_TASK_ASSIGNMENT_STATUS_DICT['DE-ASSIGN-FAIL']: (ROUTE_TASK_ASSIGNMENT_STATUS_DICT['IN-PROGRESS'],),
        ROUTE_TASK_ASSIGNMENT_STATUS_DICT['IN-PROGRESS']: (ROUTE_TASK_ASSIGNMENT_STATUS_DICT['STARTED'],
                                                           ROUTE_TASK_ASSIGNMENT_STATUS_DICT['NOT-DISPATCHED'],
                                                           ROUTE_TASK_ASSIGNMENT_STATUS_DICT['PARTIAL'],
                                                           ROUTE_TASK_ASSIGNMENT_STATUS_DICT['ASSIGN-FAIL'],
                                                           ROUTE_TASK_ASSIGNMENT_STATUS_DICT['DE-ASSIGN-FAIL'],),
        ROUTE_TASK_ASSIGNMENT_STATUS_DICT['STARTED']: (ROUTE_TASK_ASSIGNMENT_STATUS_DICT['DISPATCHED'],
                                                       ROUTE_TASK_ASSIGNMENT_STATUS_DICT['IN-PROGRESS'],),
        ROUTE_TASK_ASSIGNMENT_STATUS_DICT['DISPATCHED']: (ROUTE_TASK_ASSIGNMENT_STATUS_DICT['COMPLETED'],
                                                          ROUTE_TASK_ASSIGNMENT_STATUS_DICT['IN-PROGRESS'],),
        ROUTE_TASK_ASSIGNMENT_STATUS_DICT['COMPLETED']: (ROUTE_TASK_ASSIGNMENT_STATUS_DICT['ARCHIVED'],),
    }

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    read_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=False, blank=False)
    meter_reader_id = models.BigIntegerField(null=True, blank=True)
    schedule_log_id = models.BigIntegerField(null=True, blank=True)
    consumer_meter_json = JSONField(null=True, blank=True)
    state = models.IntegerField(choices=ROUTE_TASK_ASSIGNMENT_STATUS, default=0)
    assign_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False) # use for reading complete or not
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    @property
    def get_read_cycle_name(self):
        read_cycle = get_read_cycle_by_id(self.read_cycle_id)
        return read_cycle

    @property
    def get_route_name(self):
        route = get_route_by_id(self.route_id)
        return route

    @property
    def get_meter_reader_name(self):
        meter_reader = get_user_by_id(self.meter_reader_id)
        return meter_reader

    @property
    def get_schedule_log(self):
        schedule_log = get_schedule_log_by_id(self.schedule_log_id)
        return schedule_log

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return str(self.id_string)

    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            self.save()
        except Exception as ex:
            raise CustomAPIException(ROUTE_TASK_ASSIGNMENT_TRANSITION, status_code=status.HTTP_412_PRECONDITION_FAILED)

# Create Schedule Table end


def get_route_task_assignment_by_id(id):
    try:
        return RouteTaskAssignment.objects.get(id=id, is_active=True)
    except:
        return False


def get_route_task_assignment_by_id_string(id_string):
    try:
        return RouteTaskAssignment.objects.get(id_string=id_string, is_active=True)
    except:
        return False
