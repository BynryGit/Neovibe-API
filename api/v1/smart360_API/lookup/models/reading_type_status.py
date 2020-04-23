# Table Header : Reading Type Status
# Table Type : Lookup (Local)
# Table Name : 2.12.60 Reading Type Status
# Description : It store the reading type status with respect to the reading type.
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : 2.3.8.6 Reading Additional parameters
# Auther : Jayshree
# Creation Date : 22/04/2020

import datetime
import uuid
from django.db import models

# Start the Code
class ReadingTypeStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    reading_type_status = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.reading_type_status

    def __unicode__(self):
        return self.reading_type_status
# End the code