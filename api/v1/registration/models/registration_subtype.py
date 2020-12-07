# table Header :
# module: S&M, Consumer Care & Ops | sub-module - Registrations
# table type: lookup (local)
# table name: 2.12.46 Registration SubType
# table description: A lookup table that stores the various Sub types of registrations
# frequency of data changes: low
# sample table data:
# reference tables: 2.3.2. Consumer - Registration
# Author: Chinmay Pathak
# creation date: 30/11/2020

# change history
#<ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from v1.registration.models.registration_type import get_registration_type_by_id

#Create Registration Type table start
class RegistrationSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    registration_type_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    
    @property
    def get_registration_type(self):
        registration_type = get_registration_type_by_id(self.registration_type_id)
        return registration_type


def get_registration_subtype_by_id_string(id_string):
    return RegistrationSubType.objects.get(id_string = id_string)


def get_registration_subtype_by_id(id):
    return RegistrationSubType.objects.filter(id = id)

    # Create Registration Type table end