# table Header :
# module: S&M, Consumer Care & Ops | sub-module - Registrations
# table type: lookup (local)
# table name: 2.12.46 Registration Type
# table description: A lookup table that stores the various types of registrations
# frequency of data changes: low
# sample table data:
# reference tables: 2.3.2. Consumer - Registration
# Author: Gauri
# creation date: 22/4/2020

# change history
#<ddmmyyyy>-<changes>-<Author>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database

#Create Registration Type table start
class RegistrationType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    name = models.CharField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

def get_registration_type_by_id_string(id_string):
    return RegistrationType.objects.get(id_string=id_string)

    # Create Registration Type table end