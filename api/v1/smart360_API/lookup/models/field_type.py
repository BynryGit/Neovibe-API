# table header
# table type : lookup (Local)
# table name : 2.12.35 Field Type
# table description : A lookup table for various types of fields.
# frequency of data changes : LOW
# sample tale data : "meter no" , "address" , "connection status"
# reference tables : 2.3.4 Survey Consumer Table , 2.6.3 SOP Master Details , 2.6.7 Closure Report Transaction
# author : Saloni
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Field Type table start.

class FieldType(models.Model):
    id_string = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    type = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.CharField(blank=False, null=False)
    updated_by = models.CharField(blank=False, null=False)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.type

# Create Field Type table end.
