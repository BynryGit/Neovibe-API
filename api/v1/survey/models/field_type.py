# table header
# module: S&M, | sub-module - Survey
# table type : lookup (local)
# table name : 2.12.35 Field Type
# table description : A lookup table for various types of fields in given survey .
# frequency of data changes : low
# sample tale data : "meter no" , "address" , "connection status"
# reference tables : 2.3.4 Survey Consumer Table , 2.6.3 SOP Master Details , 2.6.7 Closure Report Transaction
# author : Saloni Monde
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Field Type table start.

class FieldType(models.Model):
    id_string = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Field Type table end.
