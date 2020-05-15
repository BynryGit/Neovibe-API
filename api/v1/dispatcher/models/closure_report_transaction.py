# table header
# module: O&M
# table type : Master
# table name : 2.6.7 Closure Report Transaction
# table description : It will store all the main sop related stuff with respect to service appointment
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

# Create Closure Report Transaction table start

class ClosureReportTransaction(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_type = models.BigIntegerField(null=True, blank=True)
    closure_report = models.BigIntegerField(null=True, blank=True)
    sop_master = models.BigIntegerField(null=True, blank=True)
    sop_master_detail = models.BigIntegerField(null=True, blank=True)
    task = models.BigIntegerField(null=True, blank=True)
    field_type = models.BigIntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=200, blank=True, null=True)
    field_value = models.CharField(max_length=200, blank=True, null=True)
    flag = models.BooleanField(default=False)
    sop_status = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.closure_report)

    def __unicode__(self):
        return str(self.closure_report)

# Create Closure Report Transaction table end.
