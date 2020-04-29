# table header
# module: Utility | sub-module - All
# table type : Master
# table name : 2.1  Utility Master
# table description : It is Utility Master table. It will contain details for Utility details
# frequency of data changes : Low
# sample tale data : "BGL",
# reference tables :
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database


# Create Utility Master table start.

class UtilityMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    short_name = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    phone_no = models.BigIntegerField(null=True, blank=True)
    email_id = models.CharField(max_length=200, blank=False, null=False)
    region_id = models.BigIntegerField(null=True, blank=True)
    country_id = models.BigIntegerField(null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

def get_utility_by_id_string(id_string):
    return UtilityMaster.objects.get(id_string = id_string)

# Create Utility Master table end.
