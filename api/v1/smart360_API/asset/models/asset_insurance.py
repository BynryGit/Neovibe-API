# table header
# module: Asset
# table type : Master
# table name : 2.6.2.2 Asset Insurance
# table description : It will store insurance for asset
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


# Create Asset Insurance table start

class AsssetInsurance(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    insurance_no = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    provider = models.CharField(max_length=200, blank=True, null=True)
    cost = models.CharField(max_length=200, blank=True, null=True)
    effective_start_date = models.DateField(null=True, blank=True, default=datetime.now())
    effective_end_date = models.DateField(null=True, blank=True, default=datetime.now())
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.insurance_no

    def __unicode__(self):
        return self.insurance_no

# Create Asset Insurance table end.
