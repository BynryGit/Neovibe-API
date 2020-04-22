# # Table Header : Meter Image Type
# Table Type : Lookup (Local)
# Table Name : 2.12.58 Meter Image Type
# Description : Meter Image Type and ID of Meter Image Type to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : 2.3.8.5 Meter Reading Images
# Auther : Jayshree
# Creation Date : 21-04-2020

import datetime
import uuid
from django.db import models


# Start the Code
class MeterImageType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    meter_image_type = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.meter_image_type

    def __unicode__(self):
        return self.meter_image_type
# End the Code