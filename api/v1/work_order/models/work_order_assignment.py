from datetime import datetime # importing package for datetime
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField

# Create Service Master table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


# table header
# module: Work Order | sub-module -
# table type: Master
# table name: WorkOrderAssignment
# table description: It contains the list of WorkOrderAssignment
# #frequency of data changes: high
# sample table data:
# reference tables:
# Author : Priyanka Kachare
# Creation Date : 16/12/2020

class WorkOrderAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    sa_id = models.BigIntegerField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    assignment_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    assignment_time = models.TimeField()
    completion_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    completion_time = models.TimeField()
    TAT = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    status = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.sa_id

    def __unicode__(self):
        return self.sa_id

# Create work_order_master table end

def get_work_order_assignment_by_tenant_id_string(id_string):
    return WorkOrderAssignment.objects.filter(tenant__id_string=id_string)


def get_work_order_assignment_by_utility_id_string(id_string):
    return WorkOrderAssignment.objects.filter(utility__id_string=id_string)


def get_work_order_assignment_by_id(id):
    try:
        return WorkOrderAssignment.objects.get(id=id)
    except:
        return False


def get_work_order_assignment_by_id_string(id_string):
    try:
        return WorkOrderAssignment.objects.get(id_string=id_string)
    except:
        return False

