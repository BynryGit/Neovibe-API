# table header
# module: Asset, Finance | sub-module - assets, Finance
# table type : lookup (Global)
# table name : 2.12.80 Deprecation Method
# table description : A lookup table for different deprecation methods.
# frequency of data changes : Low
# sample tale data :
# reference tables : 2.6.2.2 Asset Master
# author : Saloni
# created on : 22/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Deprecation Method table start.

class DeprecationMethod(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    method = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.CharField(blank=False, null=False)
    updated_by = models.CharField(blank=False, null=False)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.method

# Create Deprecation Method table end.

