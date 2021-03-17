# table header
# module: Utility | sub-module - All
# table type : Master
# table name : Mandatory Fields
# table description :  It will contain details for Utility Status
# frequency of data changes : Low
# sample table data : "Activate", "Deactive"
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
from django.utils import timezone # importing package for datetime


#Create Utility Status table start

class UtilityStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

 # Create Utility Status table end


def get_utility_status_by_id(id):
    try:
        return UtilityStatus.objects.get(id = id)
    except:
        return False


def get_utility_status_by_id_string(id_string):
    try:
        return UtilityStatus.objects.get(id_string = id_string)
    except:
        return False