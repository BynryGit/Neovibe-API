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
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

from django.db import models  # importing package for database


# Create Service Details Table Start.

class ServiceDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_request_no = models.CharField(max_length=200, null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    service_request = models.BigIntegerField(null=True, blank=True)
    service_type = models.BigIntegerField(null=True, blank=True)
    consumer_remark = models.CharField(max_length=500, null=True, blank=True)
    admin_remark = models.CharField(max_length=500, null=True, blank=True)
    request_date = models.DateField(null=True, blank=True, default=datetime.now())
    request_due_date = models.DateField(null=True, blank=True, default=datetime.now())
    request_channel = models.BigIntegerField(null=True, blank=True)
    is_field_appointment = models.BooleanField(default=False)
    status = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.service_request_no

    def __unicode__(self):
        return self.service_request_no

# Create Service Details table end.
