import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField

# Create work_order Master table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime


# table header
# module: Work Order | sub-module -
# table type: Master
# table name:Utility Leave Type
# table description: It contains the list of Leave Types
# #frequency of data changes: Low
# sample table data:'Paid','Birthday','Restricted Holiday'
# reference tables:
# Author : Chinmay Pathak
# Creation Date : 29/12/2020

class UtilityLeaveType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    leave_type = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.leave_type

    def __unicode__(self):
        return self.leave_type


# Create work_order_master table end

def get_utility_leave_by_tenant_id_string(id_string):
    return UtilityLeaveType.objects.filter(tenant__id_string=id_string)


def get_utility_leave_by_utility_id_string(id_string):
    return UtilityLeaveType.objects.filter(utility__id_string=id_string)


def get_utility_leave_by_id(id):
    try:
        return UtilityLeaveType.objects.get(id=id)
    except:
        return False


def get_utility_leave_by_id_string(id_string):
    try:
        return UtilityLeaveType.objects.get(id_string=id_string)
    except:
        return False