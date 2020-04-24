# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.2. Role Privileges
# table description : A master table that stores privileges of users.
# frequency of data changes : Low
# sample tale data : "view only", "validation 1", "validation 2"
# reference tables : 2.5.4 Product/Services Table
# author : Saloni Monde
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Role Privilege table start

class RolePrivilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    role = models.IntegerField(null=False, blank=False)
    department = models.CharField(max_lengt=200, null=True, blank=True)
    role_type = models.IntegerField(null=False, blank=False)
    module = models.IntegerField(null=False, blank=False)
    sub_module = models.IntegerField(null=False, blank=False)
    form_factor = models.IntegerField(null=False, blank=False)
    status = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.role_type

    def __unicode__(self):
        return self.role_type

# Create Role Privilege table end
