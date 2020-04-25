# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.1. Role Master
# table description : A role master to store all roles for users.
# frequency of data changes : Low
# sample tale data : "admin","super admin", "vendor"
# reference tables : 2.5.4 Product/Services Table
# author : Saloni Monde
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Role Master table start

class Role(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_lengt=200, null=True, blank=True)
    department = models.CharField(max_lengt=200, null=True, blank=True)
    form_factor = models.IntegerField(null=False, blank=False)
    status = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Role Master table end
