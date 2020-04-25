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

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database

from api.v1.smart360_API.lookup.models.activity import Activity


# TODO: correct the spelling :Done
# Create Privilege table start

class Privilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    name = models.CharField(max_length=500, null=False, blank=False)
    activity = models.ForeignKey(Activity, null=False, blank=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Privilege table end


def get_privilege_by_id(id):
    return Privilege.objects.get(id=id)
