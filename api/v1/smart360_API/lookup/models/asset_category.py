# table header
# module: O&M, Assets, Purchase, Store, Tender, Contract | sub-module - All
# table type : lookup (Local)
# table name : 2.12.85 Asset Category
# table description : A lookup table for categories of assets.
# frequency of data changes : Low
# sample table data : Meter, CNG Station, Pipe
# reference tables : 2.6.2.2 Asset Master
# author : Saloni Monde
# created on : 22/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Asset Category table start

class AssetCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    category = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.CharField(blank=False, null=False)
    updated_by = models.CharField(blank=False, null=False)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category

    def __unicode__(self):
        return self.category

# Create Asset Category table end.
