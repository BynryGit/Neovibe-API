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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Closure Report Transaction table start

class ClosureReportTransaction(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    service_type_id = models.IntegerField(null=True, blank=True)
    closure_report_id = models.IntegerField(null=True, blank=True)
    sop_master_id = models.IntegerField(null=True, blank=True)
    sop_master_detail_id = models.IntegerField(null=True, blank=True)
    task_id = models.IntegerField(null=True, blank=True)
    field_type = models.IntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=200, blank=True, null=True)
    field_value = models.CharField(max_length=200, blank=True, null=True)
    flag = models.BooleanField(default=False)
    sop_status_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(str(self.id))

# Create Closure Report Transaction table end.