# table header
# table type : lookup (Local)
# table name : 2.12.66 Product/Services Sub-Category
# table description : A lookup table for sub-categories of products and services.
# frequency of data changes : Low
# sample tale data :
# reference tables : 2.5.4 Product/Services Table
# author : Saloni
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Product Service Sub Category table start.

class ProductServiceSubCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    sub_category = models.CharField(max_length=200, blank=False, null=False)
    category = models.CharField(blank=False, null=False)
    created_by = models.CharField(blank=False, null=False)
    updated_by = models.CharField(blank=False, null=False)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.sub_category

# Create Product Service Sub Category table end.
