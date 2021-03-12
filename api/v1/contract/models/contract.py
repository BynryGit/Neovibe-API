# table header
# module: Sourcing, Purchase
# table type : Master
# table name : Contract
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

from v1.contract.models.contract_period import get_contract_period_by_id
from v1.contract.models.contract_status import get_contract_status_by_id
from v1.contract.models.contract_type import get_contract_type_by_id
from v1.supplier.models.supplier import get_supplier_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from decimal import Decimal  # importing package for decimal
from django.utils import timezone # importing package for datetime


# Create Contracts Master Table start

class Contract(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    contract_type = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    contract_period = models.BigIntegerField(null=True, blank=True)
    contract_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    supplier = models.BigIntegerField(null=True, blank=True)
    supplier_product_id = models.BigIntegerField(null=True, blank=True)
    cost_center = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_supplier(self):
        supplier = get_supplier_by_id(self.supplier)
        return supplier

    @property
    def get_contract_type(self):
        contract = get_contract_type_by_id(self.contract_type)
        return contract

    @property
    def get_contract_period(self):
        period = get_contract_period_by_id(self.contract_period)
        return period

    @property
    def get_contract_status(self):
        status = get_contract_status_by_id(self.status)
        return status

# Create Contracts Master table end.


def get_contract_by_id(id):
    try:
        return Contract.objects.get(id=id)
    except:
        return False


def get_contract_by_id_string(id_string):
    try:
        return Contract.objects.get(id_string=id_string)
    except:
        return False


def get_supplier_contract_by_id(id):
    try:
        return Contract.objects.get(supplier=id)
    except:
        return False