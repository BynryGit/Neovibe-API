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
import datetime  # importing package for datetime

from django.db import models  # importing package for database

from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster


# Create User Privilege table start

class UserPrivilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    user = models.IntegerField(null=False, blank=False)
    module = models.IntegerField(null=False, blank=False)
    sub_module = models.IntegerField(null=False, blank=False)
    privilege = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id

# Create User Privilege table end
