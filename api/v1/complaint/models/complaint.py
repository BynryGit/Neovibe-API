import uuid  # importing package for guid
from datetime import datetime
from v1.complaint.models.complaint_sub_type import get_complaint_sub_type_by_id
from v1.consumer.models.consumer_service_contract_details import ConsumerServiceContractDetail # importing package for datetime
import fsm
from rest_framework import status

from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id
from django.utils import timezone # importing package for datetime
from v1.complaint.models.consumer_complaint_master import get_consumer_complaint_master_by_id
from v1.complaint.models.complaint_sub_type import get_complaint_sub_type_by_id
from v1.complaint.models.complaint_type import get_complaint_type_by_id

# *********** COMPLAINT CONSTANTS **************
COMPLAINT_DICT = {
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

# Table Header
# Module : Consumer Care & Ops | Sub-Module : Consumer Complaints
# Module: Consumer Care | sub-module : Complaints
# Table Type : Master (Global)
# Table Name : 2.4.5. Consumer - Complaints
# Description : it will contain the list of complaint request raised by the consumer with its status, request etc.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


# Create Consumer Complaints Table Start.
class Complaint(models.Model, fsm.FiniteStateMachineMixin):
    CHOICES = (
        (0,  'CREATED'),
        (1,  'ACCEPTED'),
        (2,  'REJECTED'),
        (3,  'IN PROGRESS'),
        (4,  'NOT ASSIGNED'),
        (5,  'ASSIGNED'),
        (6,  'COMPLETED'),
        (7,  'HOLD'),
        (8,  'CLOSED'),
        (9,  'FAILED'),
        (10, 'ARCHIVED'),
    )

    state_machine = {
        COMPLAINT_DICT['CREATED']        : (COMPLAINT_DICT['NOT ASSIGNED'],COMPLAINT_DICT['IN PROGRESS'],COMPLAINT_DICT['COMPLETED'], COMPLAINT_DICT['REJECTED'], COMPLAINT_DICT['HOLD']),
        COMPLAINT_DICT['ACCEPTED']       : (COMPLAINT_DICT['COMPLETED'],),
        COMPLAINT_DICT['REJECTED']       : (COMPLAINT_DICT['ASSIGNED'],),
        COMPLAINT_DICT['IN PROGRESS']    : (COMPLAINT_DICT['REJECTED'], COMPLAINT_DICT['HOLD'],),
        COMPLAINT_DICT['NOT ASSIGNED']   : (COMPLAINT_DICT['FAILED'], COMPLAINT_DICT['IN PROGRESS'], COMPLAINT_DICT['ASSIGNED']),
        COMPLAINT_DICT['ASSIGNED']       : (COMPLAINT_DICT['ACCEPTED'], COMPLAINT_DICT['REJECTED'],),
        COMPLAINT_DICT['COMPLETED']      : (COMPLAINT_DICT['HOLD'], COMPLAINT_DICT['CLOSED'],),
        COMPLAINT_DICT['HOLD']           : (COMPLAINT_DICT['ASSIGNED'], COMPLAINT_DICT['CLOSED'], COMPLAINT_DICT['IN PROGRESS'],COMPLAINT_DICT['COMPLETED'], COMPLAINT_DICT['REJECTED']),
        COMPLAINT_DICT['CLOSED']         : (COMPLAINT_DICT['ARCHIVED'],),
        COMPLAINT_DICT['ARCHIVED']       : (COMPLAINT_DICT['ARCHIVED'],),
    }
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    complaint_no = models.CharField(max_length=200, null=True, blank=True)
    complaint_name = models.CharField(max_length=500, null=True, blank=True)
    consumer_service_contract_detail_id = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=3000, null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    consumer_complaint_master_id = models.BigIntegerField(null=True, blank=True)
    complaint_type_id = models.BigIntegerField(null=True, blank=True)
    complaint_sub_type_id = models.BigIntegerField(null=True, blank=True)
    complaint_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    channel = models.BigIntegerField(null=True, blank=True)
    consumer_remark = models.CharField(max_length=500, null=True, blank=True)
    admin_remark = models.CharField(max_length=500, null=True, blank=True)
    complaint_raised_by = models.BigIntegerField(null=True, blank=True)
    state = models.BigIntegerField(choices=CHOICES, default=0)
    close_date = models.DateTimeField(null=True, blank=True)
    closure_remark = models.CharField(max_length=500, null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

    @property
    def get_consumer_service_contract_detail_id(self):
        consumer_service_contract_detail = get_consumer_service_contract_detail_by_id(self.consumer_service_contract_detail_id)
        return consumer_service_contract_detail

    @property
    def get_complaint_master_id(self):
        complaint_master = get_consumer_complaint_master_by_id(self.consumer_complaint_master_id)
        return complaint_master

    @property
    def get_complaint_type(self):
        return get_complaint_type_by_id(self.complaint_type_id)

    @property
    def get_complaint_sub_type(self):
        complaint_sub_type = get_complaint_sub_type_by_id(id=self.complaint_sub_type_id)
        return complaint_sub_type
    
    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            self.save()
        except Exception as e:
            raise CustomAPIException("Complaint transition failed", status_code=status.HTTP_412_PRECONDITION_FAILED)
    

# Create Consumer Complaints table end.

def get_consumer_complaints_by_consumer_no(consumer_no):
    try:
        return Complaint.objects.filter(consumer_no = consumer_no)
    except:
        return False


def get_consumer_complaint_by_id_string(id_string):
    try:
        return Complaint.objects.get(id_string = id_string)
    except:
        return False


def get_consumer_complaint_by_id(id):
    try:
        return Complaint.objects.get(id = id)
    except:
        return False