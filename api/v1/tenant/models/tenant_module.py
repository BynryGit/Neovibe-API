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
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.module

    def __unicode__(self):
        return self.module

# Create Tenant  Module table end.

def get_tenant_module_by_id(id):
    try:
        return TenantModule.objects.get(id = id)
    except:
        return False


def get_tenant_module_by_id_string(id_string):
    try:
        return TenantModule.objects.get(id_string = id_string)
    except:
        return False


def get_tenant_modules_by_tenant_id_string(id_string):
    return TenantModule.objects.filter(tenant__id_string = id_string)


def get_tenant_modules_by_utility_id_string(id_string):
    return TenantModule.objects.filter(utility__id_string = id_string)