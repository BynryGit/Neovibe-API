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


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

from django.db import models  # importing package for database


# Create Consumer Complaints Table Start.

class ConsumerComplaints(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    complaint_no = models.CharField(max_length=200, null=True, blank=True)
    complaint_name = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    complaint_type_id = models.BigIntegerField(null=True, blank=True)
    complaint_sub_type_id = models.BigIntegerField(null=True, blank=True)
    complaint_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    channel = models.BigIntegerField(null=True, blank=True)
    consumer_remark = models.CharField(max_length=500, null=True, blank=True)
    admin_remark = models.CharField(max_length=500, null=True, blank=True)
    complaint_raised_by = models.BigIntegerField(null=True, blank=True)
    complaint_status_id = models.BigIntegerField(null=True, blank=True)
    close_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    closure_remark = models.CharField(max_length=500, null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.complaint_no

    def __unicode__(self):
        return self.complaint_no
# Create Consumer Complaints table end.

def get_consumer_complaints_by_consumer_no(consumer_no):
    try:
        return ConsumerComplaints.objects.filter(consumer_no = consumer_no)
    except:
        return False


def get_consumer_complaint_by_id_string(id_string):
    try:
        return ConsumerComplaints.objects.get(id_string = id_string)
    except:
        return False


def get_consumer_complaint_by_id(id):
    try:
        return ConsumerComplaints.objects.get(id = id)
    except:
        return False
