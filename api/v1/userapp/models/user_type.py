# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (local)
# Table Name : 2.12.17 User Type
# Description : It is a global lookup table that stores various types of users
# Frequency of data changes : Low
# Sample Table Data : "Employee" ,  "Vendor" , "Supplier"
# Reference Table : 2.5.5 User Documents.
# Author : Jayshree Kumbhare
# Creation Date : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create User Type table start

class UserType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

# Create User Type table end


def get_user_type_by_id_string(id_string):
    return UserType.objects.filter(id_string=id_string).last()


def get_user_type_by_id(id):
    return UserType.objects.filter(id=id).last()
