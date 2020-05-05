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

from datetime import datetime # importing package for datetime
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Sub Module table start


class SubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # sub_module = models.BigIntegerField(null=False, blank=False)
    module_id = models.BigIntegerField(null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# Create Sub Module table end

def get_sub_module_by_id(id):
    return SubModule.objects.get(id=id,is_active=True)


def get_submodule_by_module_id(id):
    return SubModule.objects.filter(module_id=id,is_active=True)


def get_sub_module_by_id_string(id_string):
    return SubModule.objects.filter(id_string=id_string,is_active=True)