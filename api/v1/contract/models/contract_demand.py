# table header
# module: Sourcing
# table type : Master
# table name : Contract Demand
# table description : The Contracts Demand table saves the basic details of Contract Demand
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from decimal import Decimal  # importing package for float number


# Create Contracts Demand Table start

class ContractDemand(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    contract = models.BigIntegerField(null=True, blank=True)
    supplier_product = models.BigIntegerField(null=True, blank=True)
    requested_quantity = models.BigIntegerField(null=True, blank=True)
    unit = models.BigIntegerField(null=True, blank=True)
    actual_quantity = models.BigIntegerField(null=True, blank=True)
    rate = models.FloatField(max_length=200, blank=False, null=False, default=Decimal(0.00))
    demand_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    due_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    remark = models.CharField(max_length=500, blank=True, null=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    gate_pass_id = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.contract

    def __unicode__(self):
        return self.contract

# Create Contracts Demand table end.


def get_contract_demand_by_id(id):
    try:
        return ContractDemand.objects.get(id = id)
    except:
        return False


def get_contract_demand_by_id_string(id_string):
    try:
        return ContractDemand.objects.get(id_string = id_string)
    except:
        return False
