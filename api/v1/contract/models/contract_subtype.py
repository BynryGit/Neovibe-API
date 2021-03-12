# table header
# module: Sourcing  | sub-module - Contract
# table type : lookup (Local)
# table name : 2.12.70 Contract Type
# table description : A lookup table for subtypes of contracts.
# frequency of data changes : Low
# sample tale data :"Valid Contract", "Voidable Contract"
# reference tables : 2.5.6 Contracts Master Table
# author : Gaurav
# created on : 10/11/2020

# change history
# <ddmmyyyy><changes><author>



import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.contract.models.contract_type import get_contract_type_by_id
from django.utils import timezone # importing package for datetime

# Create Contract SubType table start.

class ContractSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    type_id = models.BigIntegerField(null=True, blank=True)	
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_contract_type(self):
        contract_type = get_contract_type_by_id(self.type_id)
        return contract_type


# Create Contract SubType table end.


def get_contract_subtype_by_id(id):
    try:
        return ContractSubType.objects.get(id=id)
    except:
        return False

def get_contract_subtype_by_id_string(id_string):
    try:
        return ContractSubType.objects.get(id_string=id_string)
    except:
        return False

