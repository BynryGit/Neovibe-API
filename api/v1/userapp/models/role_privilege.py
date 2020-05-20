# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.2. Role Privileges
# table description : A master table that stores role wise privileges.
# frequency of data changes : Low
# sample tale data : "view only", "validation 1", "validation 2"
# reference tables : 2.5.4 Product/Services Table
# author : Saloni Monde
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

# from v1.commonapp.models.sub_module import get_submodule_by_module_id
from v1.commonapp.models.module import get_module_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.userapp.models.privilege import get_privilege_by_id
from v1.userapp.models.role import get_role_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Role Privilege table start

class RolePrivilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    role_id = models.BigIntegerField(null=True, blank=True)
    module_id = models.BigIntegerField(null=True, blank=True)
    sub_module_id = models.BigIntegerField(null=True, blank=True)
    privilege_id = models.BigIntegerField(null=True, blank=True) # View, Edit
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.tenant.name

    def __unicode__(self):
        return self.tenant.name

    @property
    def get_all_submodules(self):
        return  True

    @property
    def get_role(self):
        return get_role_by_id(self.role_id)

    @property
    def get_module(self):
        return get_module_by_id(self.module_id)

    @property
    def get_sub_module(self):
        return get_sub_module_by_id(self.sub_module_id)

    @property
    def get_privilege(self):
        return get_privilege_by_id(self.privilege_id)

    # Create Role Privilege table end


def get_role_privilege_by_role_id(id):
    return RolePrivilege.objects.filter(role_id=id, is_active=True)


def get_role_privilege_by_id_string(id_string):
    return RolePrivilege.objects.filter(id=id_string, is_active=True).last()


def get_privilege_by_sub_module_id(sub_module_id,module_id):
    privilege = RolePrivilege.objects.filter(module_id=module_id,sub_module_id=sub_module_id).last()
    return get_privilege_by_id(privilege.privilege_id)