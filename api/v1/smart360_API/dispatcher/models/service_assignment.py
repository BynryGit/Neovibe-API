# table header
# module: O&M
# table type : Master
# table name : 2.6.4 Service Assignment
# table description :It will store the assign,deassign,reassign records of all service appointment.
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


# Create Service Assignment table start

class ServiceAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    service_request_id = models.IntegerField(null=True, blank=True)
    service_type_id = models.IntegerField(null=True, blank=True)
    resource_id = models.IntegerField(null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    area_id = models.IntegerField(null=True, blank=True)
    parent_record_id = models.IntegerField(null=True, blank=True)
    status_id = models.IntegerField(null=True, blank=True)
    assigned_date = models.DateField(null=True, blank=True, default=datetime.now())
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    completion_date = models.DateField(null=True, blank=True, default=datetime.now())
    defined_duration = models.CharField(max_length=200, blank=True, null=True)
    actual_duration = models.CharField(max_length=200, blank=True, null=True)
    is_complete_on_time = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(str(self.id))

# Create Service Assignment table end.

