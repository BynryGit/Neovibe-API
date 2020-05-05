# table header
# module: Utility | sub-module - Utility Service
# table type : Master
# table name : Mandatory Fields
# table description :  It will contain details for Mandatory Fields
# frequency of data changes : Low
# sample tale data :
# reference tables :
# author : Gauri Deshmukh
# created on : 27/04/2020

# change history
# <ddmmyyyy><changes><author>




import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime

from django.db import models  # importing package for database
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

# Create Mandatory Fields table start.
class UtilityMandetoryFields(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    field_id = models.BigIntegerField(null=True, blank=True)
    is_mandatory = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())


def __str__(self):
    return self.field_id


def __unicode__(self):
    return self.field_id

# Create  Mandatory Fields table end.
