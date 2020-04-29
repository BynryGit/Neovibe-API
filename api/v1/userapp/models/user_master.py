# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.3. User Details
# table description : A master table that stores details of all users in the system.
# frequency of data changes : Low
# sample tale data : "user1", "user2"
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
from django.contrib.auth.models import User


# Create User Details table start

class SystemUser(User):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    city = models.BigIntegerField(blank=False, null=False)
    user_type = models.BigIntegerField(null=False, blank=False)  # Tenant, Utility
    user_subtype = models.BigIntegerField(null=False, blank=False)  # employee, vendor, supplier
    form_factor_id = models.BigIntegerField(null=False, blank=False)  # Web, Mobile
    first_name = models.CharField(max_lengt=200, null=True, blank=True)
    middle_name = models.CharField(max_lengt=200, null=True, blank=True)
    last_name = models.CharField(max_lengt=200, null=True, blank=True)
    user_image = models.URLField(null=True, blank=True)
    email_id = models.CharField(max_lengt=200, null=True, blank=True)
    password = models.CharField(max_lengt=200, null=True, blank=True)
    salt = models.CharField(max_lengt=200, null=False, blank=False)
    phone_mobile = models.CharField(max_lengt=200, null=False, blank=False)
    phone_landline = models.CharField(max_lengt=200, null=False, blank=False)
    department = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.id_string

    def __unicode__(self):
        return self.id_string

# Create User Details table end
