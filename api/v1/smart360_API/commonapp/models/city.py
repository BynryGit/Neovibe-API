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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create City table start

class City(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    state = models.IntegerField(blank=False, null=False)
    country = models.IntegerField(null=True, blank=True)
    region = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create City table end


def get_city_by_id_string(id_string):
    return City.objects.get(id_string = id_string)


def get_city_by_id(id):
    return City.objects.get(id = id)

# End the Code

