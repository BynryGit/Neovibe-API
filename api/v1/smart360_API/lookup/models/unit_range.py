# table header
# module: Utility-Service  | sub-module - Service plan
# table type : lookup (Local)
# table name : 2.12.30 Unit Range
# table description : A lookup table for max unit ranges for given Service plan
# frequency of data changes : Low
# sample tale data : "50","1000"
# reference tables : 2.2.2. Service Plan Rate
# author : Saloni Monde
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Unit Range table start.

class UnitRange(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    range = models.CharField(maxlength=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
# Create Unit Range table start.

