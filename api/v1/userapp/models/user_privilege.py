# table header
# module: All  | sub-module - All
# table type :
# table name :
# table description : A master table that stores user wise privileges.
# frequency of data changes : Low
# sample tale data :
# reference tables :
# author : Saloni Monde
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.userapp.models.role_privilege import get_role_privilege_by_role_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create User Privilege table start

class UserPrivilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.BigIntegerField(null=True, blank=True)
    role_id = models.BigIntegerField(null=True, blank=True)
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
    def get_role_privilege(self):
        return get_role_privilege_by_role_id(self.role_id)

# Create User Privilege table end


def get_privilege_by_id_string(id_string):
    return UserPrivilege.objects.get(id_string=id_string, is_active=True)


def get_user_privilege_by_user_id(id):
    return UserPrivilege.objects.filter(user_id=id, is_active=True)


def get_user_privilege_by_role_id(id):
    return UserPrivilege.objects.filter(role_id=id, is_active=True)
