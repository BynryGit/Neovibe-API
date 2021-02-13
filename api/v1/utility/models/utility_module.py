__author__ = "aki"

# table header
# module: Utility | sub-module - All
# table type : Master
# table name : 2.3 Utility Module
# table description :  It will contain details of Modules available for the given Utility
# frequency of data changes : Medium
# sample tale data : "Module1"
# reference tables : 2.1 Utility Master
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.commonapp.models.module import get_module_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Utility Module table start.

class UtilityModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    subscription_id = models.BigIntegerField(null=True, blank=True)
    module_id = models.BigIntegerField(null=True, blank=True)
    label = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return str(self.label)

    def __unicode__(self):
        return str(self.label)

    @property
    def get_module(self):
        module = get_module_by_id(self.module_id)
        return module


# Create Utility Module table end.

def get_utility_module_by_module_id(module_id):
    try:
        return UtilityModule.objects.get(module_id=module_id)
    except:
        return False


def get_utility_module_by_id(id):
    try:
        return UtilityModule.objects.get(id=id)
    except:
        return False


def get_utility_module_by_id_string(id_string):
    try:
        return UtilityModule.objects.get(id_string=id_string, is_active=True)
    except:
        return False


def get_utility_modules_by_tenant_id_string(id_string):
    return UtilityModule.objects.filter(tenant__id_string=id_string)


def get_utility_modules_by_utility_id_string(id_string):
    return UtilityModule.objects.filter(utility__id_string=id_string)
