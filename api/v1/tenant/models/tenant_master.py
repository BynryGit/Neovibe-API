# table header
# module: Tenant | sub-module - All
# table type : Master - Global
# table name : 1.1 Tenant Master
# table description : It is Tenant Master table. It will contain details for Tenant
# frequency of data changes : Medium
# sample table data : MNGL,VGL,SGL
# reference tables :-
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from django.db import models  # importing package for database


# Create Tenant Master table start.

class TenantMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    short_name = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    phone_no = models.IntegerField(null=True, blank=True)
    email_id = models.CharField(max_length=200, blank=False, null=False)
    region_id = models.IntegerField(null=True, blank=True)
    country_id = models.IntegerField(null=True, blank=True)
    state_id = models.IntegerField(null=True, blank=True)
    status_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Tenant Master table end.
