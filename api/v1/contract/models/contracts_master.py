# table header
# module: Sourcing, Purchase
# table type : Master
# table name : Contracts Master
# table description : The Contracts Master table saves the basic details of any Contracts created
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
from decimal import Decimal  # importing package for decimal


# Create Contracts Master Table start

class ContractsMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    contract_type = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    end_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    contract_period = models.BigIntegerField(null=True, blank=True)
    contract_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    supplier = models.BigIntegerField(null=True, blank=True)
    product_id = models.BigIntegerField(null=True, blank=True)
    cost_center = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Contracts Master table end.
