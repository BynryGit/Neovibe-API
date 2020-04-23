# Table Header
# module : All modules & sub-modules

# Table Type : Lookup (Global)
# Table Name : 2.12.6 State
# Description : It is a global lookup table that stores the states with countries
# Frequency of data changes : Low
# Sample Table Data : Maharashtra, Assam, Bihar.
# Reference Table : 2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.7.1. Employee, 2.7.7. Branch details,
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create State table start

class State(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    country = models.IntegerField(blank=False, null=False)
    region = models.IntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create State table end


def get_state_by_id_string(id_string):
    return State.objects.get(id_string = id_string)

