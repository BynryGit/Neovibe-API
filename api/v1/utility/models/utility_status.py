# table header
# module: Utility | sub-module - All
# table type : Master
# table name : Mandatory Fields
# table description :  It will contain details for Utility Status
# frequency of data changes : Low
# sample tale data : "Activate", "Deactive"
# reference tables :
# author : Gauri Deshmukh
# created on : 27/04/2020

# change history
# <ddmmyyyy><changes><author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID

from django.db import models  # importing package for database


#Create Utility Status table start

class UtilityStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    status = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

 # Create Utility Status table end