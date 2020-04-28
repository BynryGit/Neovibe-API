# table header
# module: System
# table type : Master
# table name : 2.11.7. System - Warning
# table description : It is System table. It will contain details warnings at system level.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 27/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime
from django.db import models  # importing package for database
from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster


# Create Warning  table start

class Warning(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    module = models.IntegerField(null=True, blank=True)
    sub_module = models.IntegerField(null=True, blank=True)
    event = models.IntegerField(null=True, blank=True)
    time = models.DateField(null=True, blank=True, default=datetime.now())
    message = models.CharField(max_length=500, blank=True, null=True)
    code = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    sub_system = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id

# Create Warning end.
