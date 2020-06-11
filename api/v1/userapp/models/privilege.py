# table header
# module: Consumer Care & Ops | sub-module - Consumer, Metering & Billing
# table type: lookup
# table name: 2.12.44 Portion (Local)
# table description: It contains the list of privileges to be used by Operator or Utility
# #frequency of data changes: low
# sample table data:
# reference tables: 2.3.1. Consumer Master
# Author:
# creation date:

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster, get_tenant_by_id
from v1.utility.models.utility_master import UtilityMaster, get_utility_by_id
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# TODO: correct the spelling :Done
# Create Privilege table start

class Privilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=500, null=False, blank=False) #View,Edit
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_tenant(self):
        return get_tenant_by_id(self.tenant_id)

    @property
    def get_utility(self):
        return get_utility_by_id(self.utility_id)

# Create Privilege table end


def get_all_privilege():
    return Privilege.objects.filter(is_active=True)


def get_privilege_by_id(id):
    return Privilege.objects.filter(id=id, is_active=True).last()


def get_privilege_by_utility_id(id):
    return Privilege.objects.filter(utility_id=id, is_active=True)


def get_privilege_by_id_string(id_string):
    try:
        return Privilege.objects.get(id_string=id_string, is_active=True)
    except:
        return False


def filter_privilege_by_id_string(id_string):
    if Privilege.objects.filter(id_string=id_string, is_active=True).exists():
        return True
    else:
        return False
