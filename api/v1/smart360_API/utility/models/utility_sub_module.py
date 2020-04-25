# table header
# module: Utility | sub-module - All
# table type : Master
# table name : 2.4 Utility Module
# table description :  It will contain details of Modules available for the given Utility
# frequency of data changes : Medium
# sample tale data : "Plan - A"
# reference tables : 2.1 Utility Master, 2.3. Utility Module
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Utility Sub Module table start.

class UtilitySubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    module_id =  models.IntegerField(null=True, blank=True)
    sub_module_name  = models.CharField(max_length=200, blank=False, null=False)
    sub_module_desc  = models.CharField(max_length=500, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.id_string


    def __unicode__(self):
        return self.id_string

# Create Utility Sub Module table end.
