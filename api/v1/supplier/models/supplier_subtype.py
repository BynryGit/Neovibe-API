# table header
# table type : lookup (Local)
# table name : 2.12.70 Contract Type
# table description : A lookup table for subtypes of Supplier.
# frequency of data changes : Low
# sample tale data :"Valid Supplier", "Voidable Supplier"
# reference tables : 
# author : Gaurav 
# created on : 20/11/2020

# change history
# <ddmmyyyy><changes><author>



import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.supplier.models.supplier_type import get_supplier_type_by_id

# Create Supplier Type table start.

class SupplierSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    supplier_type_id = models.BigIntegerField(null=True, blank=True)
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
    def get_supplier_type(self):
        supplier_type = get_supplier_type_by_id(self.supplier_type_id)
        return supplier_type

# Create Supplier Type table end.


def get_supplier_subtype_by_id(id):
    try:
        return SupplierSubType.objects.get(id=id)
    except:
        return False

def get_supplier_subtype_by_id_string(id_string):
    try:
        return SupplierSubType.objects.get(id_string=id_string)
    except:
        return False
