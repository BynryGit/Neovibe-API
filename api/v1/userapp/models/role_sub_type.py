# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (local)
# Description : It is a global lookup table that stores various sub types of roles
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table :
# Author : Saloni Monde
# Creation Date : 30/04/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.userapp.models.role_type import get_role_type_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Role Sub Type table start

class RoleSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    role_type_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    @property
    def get_role_type(self):
        return get_role_type_by_id(self.role_type_id)

# Create Role Sub Type table end


def get_role_sub_type_by_tenant_id_string(id_string):
    return RoleSubType.objects.filter(tenant__id_string=id_string, is_active=True)


def get_role_sub_type_by_id_string(id_string):
    return RoleSubType.objects.filter(id_string=id_string, is_active=True).last()


def get_role_sub_type_by_id(id):
    return RoleSubType.objects.filter(id=id, is_active=True).last()


def get_sub_type_by_type_id(id):
    return RoleSubType.objects.filter(role_type_id=id, is_active=True)