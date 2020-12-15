__author__ = "Rohan"

import uuid
from datetime import datetime
import fsm
from django.db import models

from v1.complaint.models.complaint import get_consumer_complaint_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

 # Table Header
# Module : Consumer Care & Ops | Sub-Module : Complaint
# Module: Consumer Care | sub-module : Complaint
# Table Type : Transational
# Table Name : ComplaintAssignment
# Description : it will contain the list of complaint request raised by the consumer with its field operator.
# Frequency of data changes : Medium
# Sample table :
# Reference Table : Complaint
# Author : Roahan Wagh
# Creation Date : 13/07/2020
class ComplaintAssignment(models.Model, fsm.FiniteStateMachineMixin):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    complaint_id = models.BigIntegerField(null=True, blank=True)
    field_operator_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.utility.name

    def __unicode__(self):
        return self.utility.name

    @property
    def get_complaint_name(self):
        complaint = get_consumer_complaint_by_id(self.complaint_id)
        return complaint.complaint_name

    @property
    def get_complaint_id_string(self):
        complaint = get_consumer_complaint_by_id(self.complaint_id)
        return complaint.id_string

def get_complaint_assignments_by_field_operator_id(id):
    try:
        return ComplaintAssignment.objects.filter(field_operator_id = id, is_active = True)
    except Exception as e:
        return False
