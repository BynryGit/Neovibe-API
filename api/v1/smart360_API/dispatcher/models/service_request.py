# table header
# module: O&M
# table type : Master
# table name : 2.6.1 Service Request
# table description : It is service appointment table. It will store the appointment of each service type.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster

# Create Service Request table start

class ServiceRequest(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    service_type = models.IntegerField(null=True, blank=True)
    service_no = models.IntegerField(null=True, blank=True)
    service_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    consumer = models.IntegerField(null=True, blank=True)
    consumer_address = models.CharField(max_length=200, blank=True, null=True)
    asset = models.IntegerField(null=True, blank=True)
    duration = models.CharField(max_length=200, blank=True, null=True)
    parent_record = models.IntegerField(null=True, blank=True)
    city = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    subarea = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    end_date = models.DateField(null=True, blank=True, default=datetime.now())
    due_date = models.DateField(null=True, blank=True, default=datetime.now())
    effort_duration = models.CharField(max_length=200, blank=True, null=True)
    flag = models.BooleanField(default=False)
    priority = models.IntegerField(null=True, blank=True)
    skill = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return str(self.service_no) + '-' + str(self.service_name)

    def __unicode__(self):
        return str(self.service_no) + '-' + str(self.service_name)

# Create Service Request table end.


