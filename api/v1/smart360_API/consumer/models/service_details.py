# Table Header
# Module: Consumer Care
# Table Type : Master (Global)
# Table Name : 2.4.4. Service Details
# Description : It is Service table. It will contain all service details like.Utility id,service status ,etc.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Auther : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Service Details Table Start.

class ServiceDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    service_request_no = models.CharField(null=True, blank=True)
    consumer_no = models.CharField(null=True, blank=True)
    service_request_id = models.IntegerField(null=True, blank=True)
    service_type_id = models.IntegerField(null=True, blank=True)
    consumer_remark = models.CharField(null=True, blank=True)
    admin_remark = models.CharField(null=True, blank=True)
    request_date = models.DateField(null=True, blank=True, default=datetime.now())
    request_due_date = models.DateField(null=True, blank=True, default=datetime.now())
    request_channel = models.IntegerField(null=True, blank=True)
    field_appointment = models.BooleanField(default=False)
    status_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.service_request_no

    def __unicode__(self):
        return self.service_request_no

# Create Service Details table end.

