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
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Utility Sub Module table start.

class UtilitySubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    module_id =  models.BigIntegerField(null=True, blank=True)
    submodule_name  = models.CharField(max_length=200, blank=False, null=False)
    submodule_desc  = models.CharField(max_length=500, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.submodule_name


    def __unicode__(self):
        return self.submodule_name

# Create Utility Sub Module table end.
