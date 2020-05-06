# table header
# module: Utility | sub-module - All
# table type : Master
# table name :
# table description :  It will contain details of Modules available for the given Tenant
# frequency of data changes : Medium
# sample tale data : "Module1"
# reference tables :
# author : Saloni Monde
# created on : 05-05-2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database


# Create Tenant  Module table start.

class TenantModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    module = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.module

    def __unicode__(self):
        return self.module

# Create Tenant  Module table end.
