# table header
# module: Tenant | sub-module - All
# table type : Master
# table name : 1.7 Tenant System Modules
# table description : It will contain details for Tenant system modules.
# frequency of data changes : Low
# sample tale data :
# reference tables : 1.1 Tenant Master
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Tenant System Modules table start.

class TenantSystemModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    subscription_id = models.IntegerField(null=True, blank=True)
    module_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.module_id

    def __unicode__(self):
        return self.module_id

# Create Tenant System Modules table end.
