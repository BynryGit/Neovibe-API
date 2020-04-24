# Table Header : Parameter Flag Type
# Table Type : Lookup (Local)
# Table Name : 2.12.61 Parameter Flag Type
# Description : It Reading Type and ID of various Reading type to be used by Operator or Utility
# Frequency of data changes : Low
# Parameter Flag Type :
# Reference Table : 2.3.8.6 Reading Additional parameters
# Author : Jayshree
# Creation Date : 22-04-2020


import datetime
import uuid
from django.db import models

# Start the Code
class ParameterFlagType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    parameter_flag_type = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.parameter_flag_type

    def __unicode__(self):
        return self.parameter_flag_type
# End the Code