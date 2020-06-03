# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (local)
# Table Name : 2.12.17 User Type
# Description : It is a global lookup table that stores various sub types of users
# Frequency of data changes : Low
# Sample Table Data : "Employee" ,  "Vendor" , "Supplier"
# Reference Table : 2.5.5 User Documents.
# Author : Arpita Badwaik
# Creation Date : 11/05/2020


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create User Sub Type table start

class UserSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_type_id = models.BigIntegerField(null=True, blank=True)
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

    # class Meta:
        # unique_together = ('user_type_id', 'name',)

# Create User sub Type table end


def get_user_sub_type_by_id_string(id_string):
    return UserSubType.objects.filter(id_string=id_string).last()


def get_user_sub_type_by_id(id):
    return UserSubType.objects.filter(id_string=id).last()
