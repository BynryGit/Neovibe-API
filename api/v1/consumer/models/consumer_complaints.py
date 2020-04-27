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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Consumer Complaints Table Start.

class ConsumerComplaints(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    complaint_no = models.CharField(max_length=200, null=True, blank=True)
    complaint_name = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    complaint_type = models.IntegerField(null=True, blank=True)
    complaint_subtype = models.IntegerField(null=True, blank=True)
    complaint_date = models.DateField(null=True, blank=True, default=datetime.now())
    channel = models.IntegerField(null=True, blank=True)
    consumer_remark = models.CharField(max_length=500, null=True, blank=True)
    admin_remark = models.CharField(max_length=500, null=True, blank=True)
    complaint_raised_by = models.IntegerField(null=True, blank=True)
    complaint_status = models.IntegerField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True, default=datetime.now())
    closure_remark = models.CharField(max_length=500, null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.complaint_no

    def __unicode__(self):
        return self.complaint_no

# Create Consumer Complaints table end.
