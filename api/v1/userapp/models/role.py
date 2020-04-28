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
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Role Master table start

class Role(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_lengt=200, null=True, blank=True)
    role_type = models.BigIntegerField(null=False, blank=False) # Tenant, Utility
    role_subtype = models.BigIntegerField(null=False, blank=False)  # employee, vendor, supplier
    form_factor_id = models.BigIntegerField(null=False, blank=False) # Web, Mobile
    department_id = models.BigIntegerField(null=False, blank=False)
    status_id = models.BigIntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Role Master table end
