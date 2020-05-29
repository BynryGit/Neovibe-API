# table header
# module: Sourcing  | sub-module - All
# table type : lookup (Local)
# table name : Contract Status
# table description : A lookup table for contract status.
# frequency of data changes : Low
# sample tale data : "active"
# author : Akshay
# created on : 28/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Supplier Status table start.

class ContractStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Supplier Status table end.


def get_contract_status_by_id(id):
    try:
        return ContractStatus.objects.get(id=id)
    except:
        return False


def get_contract_status_by_id_string(id_string):
    try:
        return ContractStatus.objects.get(id_string=id_string)
    except:
        return False
