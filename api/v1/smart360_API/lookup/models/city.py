# Table header : City
# Table Type : Lookup (Global)
# Table Name : 2.12.7 City
# Description : It is a lookup table for all cities. it stores id and name of city with state being its foreign table.
# Frequency of data changes : Low
# Sample Table Data : "Pune", "Nagpur"
# Reference Table : 2.3.1. Consumer Master, 2.3.5 Campaign Group Table,2.3.1 Survey Table,2.7.1. Employee,
#                    2.7.7. Branch details,2.5.1. User Details,2.5.3. Vendor Details,Supplier, Contracts.
# Auther : Jayshree
# Creation Date : 21/04/2020
import datetime
import uuid
from django.db import models

# Start the Code
class City(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    city = models.CharField(max_length=20, blank=False, null=False)
    state_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.city_name

    def __unicode__(self):
        return self.city_name


def get_city_by_id_string(id_string):
    return City.objects.get(id_string = id_string)

# End the Code