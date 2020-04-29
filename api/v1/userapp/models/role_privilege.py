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
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Role Privilege table start

class RolePrivilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    role_id = models.BigIntegerField(null=False, blank=False)
    module = models.BigIntegerField(null=False, blank=False)
    sub_module = models.BigIntegerField(null=False, blank=False)
    privilege_id = models.BigIntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.roleprivilege.id

    def __unicode__(self):
        return self.self.roleprivilege.id

# Create Role Privilege table end
