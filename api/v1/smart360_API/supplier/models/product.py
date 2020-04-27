# table header
# module: Sourcing
# table type : Master
# table name : Product Table
# table description : The Product table saves the basic Product/Services details of any Supplier
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database
from decimal import Decimal  # importing package for float number

from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster


# Create Product Service Table start

class Product(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    supplier = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.UrlField(null=False, blank=False)
    category = models.IntegerField(null=True, blank=True)
    subcategory = models.IntegerField(null=True, blank=True)
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    unit = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    source_type = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Product Service table end.
