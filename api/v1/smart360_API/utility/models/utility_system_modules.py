# table header
# table type : Master
# table name :2.2  Utility System Modules
# table description : It is Utility table. It will contain details for Utility system Modules.
# frequency of data changes : Low
# sample tale data :
# reference tables :2.1. Utility Master
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Utility System Modules table start.

class UtilitySystemModules(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Utility system Modules table end.
