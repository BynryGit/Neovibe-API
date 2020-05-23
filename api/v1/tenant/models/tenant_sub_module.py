# table header
# module: Utility | sub-module - All
# table type : Master
# table name :
# table description :  It will contain details of Modules available for the given Tenant
# frequency of data changes : Medium
# sample tale data : "Sub-Module1"
# reference tables :
# author : Saloni Monde
# created on : 05-05-2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database

from v1.tenant.models.tenant_module import get_tenant_module_by_id


# Create Tenant Sub-Module table start.
class TenantSubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    sub_module_name = models.CharField(max_length=200, blank=True, null=True)
    module_id = models.BigIntegerField(null=True, blank=True)
    submodule_desc =  models.CharField(max_length=500, blank=True, null=True)
    subscription_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.sub_module_name

    def __unicode__(self):
        return self.sub_module_name

    @property
    def get_tenant_sub_module(self):
        module = get_tenant_module_by_id(self.module_id)
        return module.module_name


# Create Utility Sub Module table end.


def get_tenant_submodule_by_id(id):
    try:
        return TenantSubModule.objects.get(id=id)
    except:
        return False


def get_tenant_submodule_by_id_string(id_string):
    try:
        return TenantSubModule.objects.get(id_string=id_string)
    except:
        return False

def get_tenant_submodules_by_tenant_id_string(id_string):
    return TenantSubModule.objects.filter(tenant_id_string=id_string)


def get_tenant_submodules_by_module_id(id):
    return TenantSubModule.objects.filter(module_id=id)
