
import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField

# Create work_order Master table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

# table header
# module: Work Order | sub-module -
# table type: Master
# table name: WorkOrder Master
# table description: It contains the list of work_order
# #frequency of data changes: high
# sample table data:"Meter Installtion","meter repair"
# reference tables:
# Author : Priyanka Kachare
# Creation Date : 16/12/2020

class WorkOrderMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    work_order_number = models.BigIntegerField(null=True, blank=True)
    service_type_id = models.BigIntegerField(blank=False, null=False)
    service_subtype_id = models.BigIntegerField(blank=False, null=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    json_obj = JSONField()
    description = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create work_order_master table end

def get_work_order_master_by_tenant_id_string(id_string):
    return WorkOrderMaster.objects.filter(tenant__id_string=id_string)


def get_work_order_master_by_utility_id_string(id_string):
    return WorkOrderMaster.objects.filter(utility__id_string=id_string)


def get_work_order_master_by_id(id):
    try:
        return WorkOrderMaster.objects.get(id=id)
    except:
        return False


def get_work_order_master_by_id_string(id_string):
    try:
        return WorkOrderMaster.objects.get(id_string=id_string)
    except:
        return False
