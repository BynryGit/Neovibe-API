# table header
# module: Asset, Sourcing | sub-module - All
# table type : lookup (Local)
# table name : 2.12.65 Product/Services Category
# table description : A lookup table for categories of products and services.
# frequency of data changes : Low
# sample tale data :
# reference tables : 2.5.4 Product/Services Table
# author : Saloni Monde
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Product Service Category table start.

class SupServiceCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Product Service Category table start.


def get_supplier_service_category_by_id(id):
    try:
        return SupServiceCategory.objects.get(id = id)
    except:
        return False


def get_supplier_service_category_by_id_string(id_string):
    try:
        return SupServiceCategory.objects.get(id_string = id_string)
    except:
        return False
