# table header
# module: System
# table type : Master
# table name : 2.11.4. System - SMS Configuration
# table description : It is System table. It will contain details SMS Configuration files at system level.
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
from django.utils import timezone # importing package for datetime


# Create SMS Configuration table start

class SmsConfiguration(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    module = models.BigIntegerField(null=True, blank=True)
    sub_module = models.BigIntegerField(null=True, blank=True)
    event = models.BigIntegerField(null=True, blank=True)
    event_name = models.BigIntegerField(null=True, blank=True)
    sms_text = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id

# Create SMS Configuration end.
