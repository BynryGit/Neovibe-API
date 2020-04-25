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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Closure Report table start

class ClosureReport(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    service_request_id = models.IntegerField(null=True, blank=True)
    parent_record_id = models.IntegerField(null=True, blank=True)
    service_type_id = models.IntegerField(null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    area_id = models.IntegerField(null=True, blank=True)
    resource_id = models.IntegerField(null=True, blank=True)
    remark = field_unit = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(str(self.id))

# Create Closure Report table end.