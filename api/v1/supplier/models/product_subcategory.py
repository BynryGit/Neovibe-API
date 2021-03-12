# table header
# module: Asset, Sourcing | sub-module - All
# table type : lookup (Local)
# table name : 2.12.66 Product/Services Sub-Category
# table description : A lookup table for sub-categories of products and services.
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
from v1.supplier.models.product_category import get_supplier_product_category_by_id
from django.utils import timezone # importing package for datetime


# Create Product Service Sub Category table start.

class ProductSubCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    category = models.BigIntegerField(null=True, blank=True)
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
    def get_product_category(self):
        product_category_type = get_supplier_product_category_by_id(self.category)
        return product_category_type

# Create Product Service Sub Category table end.



def get_supplier_product_subcategory_by_id_string(id_string):
    try:
        return ProductSubCategory.objects.get(id_string = id_string)
    except:
        return False


def get_supplier_product_subcategory_by_id(id):
    try:
        return ProductSubCategory.objects.get(id = id)
    except:
        return False