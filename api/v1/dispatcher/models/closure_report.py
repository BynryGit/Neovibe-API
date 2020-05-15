# table header
# module: O&M
# table type : Master
# table name : 2.6.6 Closure Report
# table description : It will store all the information when service appointment is completed.
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


# Create Closure Report table start

class ClosureReport(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_request = models.BigIntegerField(null=True, blank=True)
    parent_record = models.BigIntegerField(null=True, blank=True)
    service_type = models.BigIntegerField(null=True, blank=True)
    city = models.BigIntegerField(null=True, blank=True)
    area = models.BigIntegerField(null=True, blank=True)
    resource = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.service_request)

# Create Closure Report table end.
