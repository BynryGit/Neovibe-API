# table header
# module: User  | sub-module - All
# table type : Master
# table name : User Detail
# table description : A master table that stores details of all User Detail.
# frequency of data changes : Low
# sample tale data :
# reference tables : User
# author :
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from django.contrib.postgres.fields import JSONField

from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create User Detail table start

class UserDetail(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.BigIntegerField(null=True, blank=True)
    json_obj = JSONField()
    description = models.CharField(max_length=200, null=False, blank=False)
    status = models.BigIntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.user_id

    def __unicode__(self):
        return self.user_id

# Create User Detail table end
