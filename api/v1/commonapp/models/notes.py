# table header
# module: Sourcing
# table type : Master
# table name : 2.5.12 Notes
# table description : The Notes table saves the Common Notes
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

# Create Notes Table start

class Notes(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    module = models.IntegerField(null=True, blank=True)
    sub_module = models.IntegerField(null=True, blank=True)
    servicetype = models.IntegerField(null=True, blank=True)
    identification = models.IntegerField(null=True, blank=True)
    note_name = models.CharField(max_length=200, blank=True, null=True)
    note_color = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.note_name

    def __unicode__(self):
        return self.note_name

# Create Notes table end.
