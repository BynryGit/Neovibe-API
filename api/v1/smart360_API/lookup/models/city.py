import datetime
import uuid
from django.db import models

# Table Type : Lookup
# Table Name : 2.12.7 City
# Description : It is a lookup table for all cities. it stores id and name of city with state being its foreign table.
# Frequency of data changes : Low
# Reference Table : 2.3.1. Consumer Master, 2.3.5 Campaign Group Table,2.3.1 Survey Table,2.7.1. Employee, 2.7.7. Branch details,2.5.1. User Details,2.5.3. Vendor Details,Supplier, Contracts.
# Auther : Jayshree
# Creation Date : 21-04-2020


class City(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    city_name = models.CharField(max_length=20, blank=False, null=False)
    state_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.city_name

    def __unicode__(self):
        return self.city_name
