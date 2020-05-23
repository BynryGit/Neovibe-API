# table header
# module: Sourcing
# table type : Master
# table name : SupplierService
# table description : The Product table saves the basic Product/Services details of any Supplier
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from decimal import Decimal  # importing package for float number


# Create Product Service Table start

class SupplierService(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    supplier = models.BigIntegerField(null=True, blank=True)
    type = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    # image = models.UrlField(null=False, blank=False)
    category = models.BigIntegerField(null=True, blank=True)
    subcategory = models.BigIntegerField(null=True, blank=True)
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    quantity = models.BigIntegerField(null=True, blank=True)
    unit = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=True, blank=True)
    source_type = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Product Service table end.


def get_supplier_service_by_id_string(id_string):
    try:
        return SupplierService.objects.get(id_string = id_string)
    except:
        return False


def get_supplier_service_by_id(id):
    try:
        return SupplierService.objects.get(id = id)
    except:
        return False