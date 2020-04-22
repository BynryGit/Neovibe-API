# table header
# table type : lookup (Local)
# table name : 2.12.71 Supplier Status
# table description : A lookup table for supplier status.
# frequency of data changes : Low
# sample tale data : "active"
# reference tables : 2.5.1 Supplier Master Table
# author : Saloni
# created on : 22/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Supplier Status table start.

class SupplierStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    status = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.CharField(blank=False, null=False)
    updated_by = models.CharField(blank=False, null=False)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.status

# Create Supplier Status table end.

