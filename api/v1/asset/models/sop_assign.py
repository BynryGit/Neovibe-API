# table header
# module: Asset
# table type : Master
# table name : 2.6.2.4 SOP Assign
# table description : It is asset sop assign table. It will store assignment according to SOP.
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


# Create SOP Assign table start

class SopAssign(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    asset_master = models.IntegerField(null=True, blank=True)
    sop_master_detail = models.IntegerField(null=True, blank=True)
    frequency = models.IntegerField(null=True, blank=True)
    city = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    subarea = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id

# Create SOP Assign table end.
