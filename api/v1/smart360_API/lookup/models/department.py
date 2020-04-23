import datetime
import uuid
from django.db import models

# Table Type : Lookup
# Table Name : 2.12.16 Department
# Description : It captures department name and ID of various department to be used by Operator or Utility
# Frequency of data changes : Low
# Reference Table : 2.7.1. Employee, 2.7.5. Employee_Positions, 2.5.1. User Details.
# Auther : Jayshree
# Creation Date : 21-04-2020


class Department(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    department_name = models.CharField(max_length=40, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.department_name

    def __unicode__(self):
        return self.department_name
