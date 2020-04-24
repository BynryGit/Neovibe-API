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
from decimal import Decimal   # importing package for float number



# Create Product Table start

class Product(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    supplier_id = models.IntegerField(null=True, blank=True)
    ps_type_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.UrlField(null=False, blank=False)
    ps_category_id = models.IntegerField(null=True, blank=True)
    ps_sub_category_id = models.IntegerField(null=True, blank=True)
    rate = models.FloatField(max_length=80, blank=False, null=False, default=Decimal(0.00))
    unit_id = models.IntegerField(null=True, blank=True)
    status_id = models.IntegerField(null=True, blank=True)
    source_type_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

# Create Product table end.