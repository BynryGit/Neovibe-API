# table header
# module: Utility | sub-module - All
# table type : Master
# table name : TenantModule
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
from v1.commonapp.models.module import get_module_by_id
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Tenant  Module table start.

class TenantModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    module_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return str(self.module_id)

    def __unicode__(self):
        return str(self.module_id)

    @property
    def get_module(self):
        module = get_module_by_id(self.module_id)
        return module

# Create Tenant  Module table end.


def get_tenant_module_by_id(id):
    try:
        return TenantModule.objects.get(id=id)
    except:
        return False


def get_tenant_module_by_id_string(id_string):
    try:
        return TenantModule.objects.get(id_string=id_string)
    except:
        return False


def get_tenant_modules_by_tenant_id_string(id_string):
    return TenantModule.objects.filter(tenant__id_string=id_string)


def get_tenant_modules_by_utility_id_string(id_string):
    return TenantModule.objects.filter(utility__id_string=id_string)