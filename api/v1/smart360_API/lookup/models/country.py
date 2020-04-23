# Table Header : Country
# Table Type : Lookup (Global)
# Table Name : 2.12.5 Country
# Description : Country and ID of Country to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : India
# Reference Table : 2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.7.7. Branch details, 2.5.3. Vendor Details
# Auther : Jayshree
# Creation Date : 21-04-2020
import datetime
import uuid
from django.db import models

# Start The Code

class Country(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    country = models.CharField(max_length=20, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.country

    def __unicode__(self):
        return self.country


def get_country_by_id_string(id_string):
    return Country.objects.get(id_string = id_string)

# End the Code
