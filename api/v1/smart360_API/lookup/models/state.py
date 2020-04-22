# Table Header : State
# Table Type : Lookup (Global)
# Table Name : 2.12.6 State
# Description : It captures State and ID of various state to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : Maharashtra, Assam, Bihar.
# Reference Table : 2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.7.1. Employee, 2.7.7. Branch details,
# Auther : Jayshree
# Creation Date : 21-04-2020

import datetime
import uuid
from django.db import models

# Start the Code
class State(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    state = models.CharField(max_length=20, blank=False, null=False)
    country_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.state

    def __unicode__(self):
        return self.state
# End the Code