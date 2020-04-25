# table header
# module: O&M
# table type : Master
# table name : 2.6.3 SOP Master Details
# table description : This table will store line items for work order with respect to main sop and service type.
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


# Create SOP Master Details table start

class SopMasterDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    sop_master = models.IntegerField(null=True, blank=True)
    service_type = models.IntegerField(null=True, blank=True)
    sub_sop_name = models.CharField(max_length=200, blank=True, null=True)
    task_type = models.IntegerField(null=True, blank=True)
    field_type = models.IntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=200, blank=True, null=True)
    field_unit = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sub_sop_name)

    def __unicode__(self):
        return str(self.sub_sop_name)

# Create SOP Master Details table end.
