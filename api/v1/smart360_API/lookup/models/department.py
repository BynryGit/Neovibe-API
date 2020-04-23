# Table Header : Department
# Table Type : Lookup (Global)
# Table Name : 2.12.16 Department
# Description : It captures department name and ID of various department to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : Marketing, Finance, Operation Management.
# Reference Table : 2.7.1. Employee, 2.7.5. Employee_Positions, 2.5.1. User Details.
# Auther : Jayshree
# Creation Date : 21-04-2020

import datetime
import uuid
from django.db import models


# Start The Code
class Department(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    department = models.CharField(max_length=40, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.department

    def __unicode__(self):
        return self.department
# End the Code