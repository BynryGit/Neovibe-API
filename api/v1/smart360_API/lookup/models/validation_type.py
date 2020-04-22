# Table Header : Validation Type
# Table Type : Lookup (Local)
# Table Name : 2.3.8.7 Validation Details
# Description : It Validation Type and ID of various Validation type to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : V1, V2
# Reference Table : 2.3.8.7 Validation Details
# Auther : Jayshree
# Creation Date : 22/04/2020

import datetime
import uuid
from django.db import models

# Start The Code
class ValidationType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    validation_type = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.validation_type

    def __unicode__(self):
        return self.validation_type
# End the Code