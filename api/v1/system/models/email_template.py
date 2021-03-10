# table header
# module: System
# table type : Master
# table name : 2.11.5. System -Email Template
# table description : It will contain details email template details to be triggered at system level.
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


# Create Email Template  table start

class EmailTemplate(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    module = models.BigIntegerField(null=True, blank=True)
    sub_module = models.BigIntegerField(null=True, blank=True)
    event = models.BigIntegerField(null=True, blank=True)
    email_template = models.CharField(max_length=200, blank=True, null=True)
    email_header = models.CharField(max_length=200, blank=True, null=True)
    email_footer = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __unicode__(self):
        return self.id

    def __unicode__(self):
        return self.id

# Create Email Template end.
