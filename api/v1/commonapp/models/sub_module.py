from datetime import datetime # importing package for datetime
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from v1.commonapp.models.module import get_module_by_id
# from v1.userapp.models.role_privilege import get_privilege_by_sub_module_id



# Table Header
# Module : All
# Table Type : Lookup (Local)
# Table Name : 2.12.3 Sub module
# Description : This table will save all the sub modules.Create Consumer Registration table start.
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : 2.6.1 Service Request
# Author :
# Creation Date :
# change history
# <ddmmyyyy>-<changes>-<Author>
class SubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sub_module = models.BigIntegerField(null=True, blank=True)
    module_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_module(self):
        return get_module_by_id(self.module_id)

    @property
    def get_privilege(self):
        return get_privilege_by_sub_module_id(self.id,self.module_id)


# Create Sub Module table end


def get_all_sub_modules():
    return SubModule.objects.filter(is_active=True)


def get_sub_module_by_id(id):
    return SubModule.objects.get(id=id,is_active=True)


def get_submodule_by_module_id(id):
    return SubModule.objects.filter(module_id=id,is_active=True)


def get_sub_module_by_id_string(id_string):
    return SubModule.objects.filter(id_string=id_string,is_active=True)