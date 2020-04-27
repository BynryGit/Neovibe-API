# table header
# module: Asset
# table type : Master
# table name : 2.6.2.3 Asset AMC Contract
# table description : It will store AMC contract.
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
from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster

# Create Asset AMC Contract table start

class AssetAmcContract(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    asset_id = models.IntegerField(null=True, blank=True)
    contract_no = models.CharField(max_length=200, blank=True, null=True)
    contract_name = models.CharField(max_length=200, blank=True, null=True)
    contract_provider = models.CharField(max_length=200, blank=True, null=True)
    cost = models.CharField(max_length=200, blank=True, null=True)
    no_of_services = models.IntegerField(null=True, blank=True)
    frequency = models.IntegerField(null=True, blank=True)
    sop = models.IntegerField(null=True, blank=True)
    effective_start_date = models.DateField(null=True, blank=True, default=datetime.now())
    effective_end_date = models.DateField(null=True, blank=True, default=datetime.now())
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.contract_no

    def __unicode__(self):
        return self.contract_no

# Create Asset AMC Contract table end.
