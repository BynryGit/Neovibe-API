# table header
# module: O&M
# table type : Master
# table name : 2.6.4 Service Assignment
# table description :It will store the assign,deassign,reassign records of all service appointment.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database

# Create Service Assignment table start

class ServiceAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_request = models.BigIntegerField(null=True, blank=True)
    service_type = models.BigIntegerField(null=True, blank=True)
    resource = models.BigIntegerField(null=True, blank=True)
    city = models.BigIntegerField(null=True, blank=True)
    area = models.BigIntegerField(null=True, blank=True)
    parent_record = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=True, blank=True)
    assigned_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    start_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    completion_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    defined_duration = models.CharField(max_length=200, blank=True, null=True)
    actual_duration = models.CharField(max_length=200, blank=True, null=True)
    is_complete_on_time = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.service_request)

    def __unicode__(self):
        return str(self.service_request)

# Create Service Assignment table end.

