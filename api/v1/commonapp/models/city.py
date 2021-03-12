# Table header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name : 2.12.7 City
# Description : It is a global lookup table that stores cities within the countries
# Frequency of data changes : Low
# Sample Table Data : "Pune", "Nagpur", "Bharatpur"
# Reference Table : 2.3.1. Consumer Master, 2.3.5 Campaign Group Table,2.3.1 Survey Table,2.7.1. Employee,
#                    2.7.7. Branch details,2.5.1. User Details,2.5.3. Vendor Details,Supplier, Contracts.
# Author : Jayshree Kumbhare
# Creation Date : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.models.state import get_state_by_id
from django.utils import timezone # importing package for datetime


# Create City table start


class City(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    state_id = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name + " " + str(self.id_string)

    def __unicode__(self):
        return self.name

    @property
    def get_state(self):
        country = get_state_by_id(self.state_id)
        return country


# Create City table end


def get_city_by_id_string(id_string):
    try:
        return City.objects.get(id_string=id_string)
    except:
        return False


def get_city_by_id(id):
    return City.objects.get(id=id)

# End the Code
