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
import datetime  # importing package for datetime

from django.db import models  # importing package for database
from decimal import Decimal  # importing package for float number

from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster


# Create Contracts Demand Table start

class ContractsDemand(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    contract = models.IntegerField(null=True, blank=True)
    product = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    rate = models.FloatField(max_length=80, blank=False, null=False, default=Decimal(0.00))
    demand = models.IntegerField(null=True, blank=True)
    demand_date = models.DateField(null=True, blank=True, default=datetime.now())
    due_date = models.DateField(null=True, blank=True, default=datetime.now())
    remark = models.CharField(max_length=500, blank=True, null=True)
    status_id = models.IntegerField(null=True, blank=True)
    fulfillment = models.IntegerField(null=True, blank=True)
    gate_pass_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.contract

    def __unicode__(self):
        return self.contract

# Create Contracts Demand table end.
