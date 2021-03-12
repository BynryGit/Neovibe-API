# table Header :
# module: S&M, Consumer Care & Ops | sub-module - Registrations
# table type: lookup (local)
# table name: 2.12.46 Registration Type
# table description: A lookup table that stores the various types of registrations
# frequency of data changes: low
# sample table data:
# reference tables: 2.3.2. Consumer - Registration
# Author: Gauri Deshmukh
# creation date: 22/4/2020

# change history
#<ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from v1.utility.models.utility_product import get_utility_product_by_id
from django.utils import timezone # importing package for datetime

#Create Registration Type table start
class RegistrationType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_utility_product(self):
        utility_product = get_utility_product_by_id(self.utility_product_id)
        return utility_product


def get_registration_type_by_id_string(id_string):
    return RegistrationType.objects.get(id_string = id_string)


def get_registration_type_by_id(id):
    return RegistrationType.objects.filter(id = id)

    # Create Registration Type table end