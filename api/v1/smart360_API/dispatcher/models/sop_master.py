# table header
# module: O&M
# table type : Master
# table name : 2.6.2 SOP Master
# table description : This table will store main sop with respect to service type.
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


# Create SOP Master table start

class SopMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    city_id = models.IntegerField(null=True, blank=True)
    service_type_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    effective_start_date = models.DateField(null=True, blank=True, default=datetime.now())
    effective_end_date = models.DateField(null=True, blank=True, default=datetime.now())
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(str(self.service_type_id) + '-' + str(self.name))

# Create SOP Master table end.
