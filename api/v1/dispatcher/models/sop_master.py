# table header
# module: O&M
# table type : Master
# table name : 2.6.2 SOP Master
# table description : This table will store main sop with respect to service type.
# frequency of data changes : High
# sample table data : "Step 1"
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


# Create SOP Master table start

class SopMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    city = models.BigIntegerField(null=True, blank=True)
    service_type = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    effective_start_date = models.DateField(null=True, blank=True, default=datetime.now())
    effective_end_date = models.DateField(null=True, blank=True, default=datetime.now())
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.service_type_id) + '-' + str(self.name)

    def __unicode__(self):
        return str(self.service_type_id) + '-' + str(self.name)

# Create SOP Master table end.
